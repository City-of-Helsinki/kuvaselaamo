palikka
.define(['jQuery'], function () {

  return window[this.id];

})
.define('docReady', ['jQuery'], function ($) {

  return palikka.defer($);

})
.define('winReady', function () {

  return palikka.defer(function (resolve) {
    window.addEventListener("load", resolve);
  });

})
.define('app.bootstrap', ['jQuery', 'docReady'], function () {

  $('#login-btn').on('click', hideModal);
  $('#signup-btn').on('click', hideModal);
  $('#account-dropdown').on('click', hideModal);
  $('#nav-collapse-btn').on('click', hideModal);

  function hideModal() {
    $('.modal').each(function() {
      if ($(this).hasClass('in')) {
        $(this).modal('hide');
      }
    });
  }

  $('.modal').on('shown.bs.modal', function() {
    $(this).find('[autofocus]').focus();
  });

  $('.modal.fade').each(function() {
    if ($(this).hasClass('error')) {
      $(this).modal('show');
    }
  });

})
.define('app.search-filter', ['jQuery', 'docReady'], function () {
  var $accordion = $('#accordion');
  var $filterLink = $('.list-group__link');
  var $searchTerm = $accordion.attr('data-search');
  var authors = [];
  var dates = [];
  var $deleteBtns = $('.search-filter__delete');
  var searchParams = '?search=' + $searchTerm;

  $('.search-filter__text').each(function() {
    authors.push($(this).attr('data-author-facet'));
    dates.push($(this).attr('data-date-facet'));
  });

  $filterLink.on('click', function() {
    var authorParam = $(this).attr('data-author-value');
    var dateParam = $(this).attr('data-date-value');
    if (typeof authorParam != 'undefined') {
      searchParams += '&author[]=' + authorParam;
    }
    if (typeof dateParam != 'undefined') {
      searchParams += '&main_date_str[]=' + dateParam;
    }
    for (var i = 0; i < authors.length; i++) {
      if (typeof authors[i] != 'undefined') {
        searchParams += '&author[]=' + authors[i];
      }
    }
    for (var i = 0; i < dates.length; i++) {
      if (typeof dates[i] != 'undefined') {
        searchParams += '&main_date_str[]=' + dates[i];
      }
    }
    window.open(searchParams, '_self');
  });

  $deleteBtns.on('click', function() {
    searchParams = '?search=' + $searchTerm;
    authors.splice(authors.indexOf($(this).attr('data-author-facet')), 1);
    dates.splice(dates.indexOf($(this).attr('data-date-facet')), 1);
    for (var i = 0; i < authors.length; i++) {
      if (typeof authors[i] != 'undefined') {
        searchParams += '&author[]=' + authors[i];
      }
    }
    for (var i = 0; i < dates.length; i++) {
      if (typeof dates[i] != 'undefined') {
        searchParams += '&main_date_str[]=' + dates[i];
      }
    }
    window.open(searchParams, '_self');
  });

})
.define('app.grid', ['jQuery', 'docReady', 'winReady'], function () {

  var $window = $(window);
  var $container = $('.flex-images');
  var $infiniteScroll = $('.flex-images.infinite-scroll');
  var $itemGroup = $('.grid__group');
  var $items = $('.flex-images .item');
  var $maxPages = $('.grid').attr('data-pages');
  var page = 1;
  var loadedImageCount = 0;
  var imageCount;

  gridInit();

  function gridInit() {
    $('.grid__group').each(function () {
      $('.flex-images .item').each(function () {
        var w = $(this).find('.flex-img').width();
        var h = $(this).find('.flex-img').height();
        if (! $(this).attr('data-w')) {
          $(this).attr('data-w', w);
          $(this).attr('data-h', h);
        }
      });
      $(this).removeClass('invisible');
    });
    if ($itemGroup.attr('data-grid-type') == 'collection') {
      $container.flexImages({
        rowHeight: 222
      });
    }
    else if ($window.width() < 450) {
      $container.flexImages({
        rowHeight: 180
      });
    }
    else {
      $container.flexImages({
        rowHeight: 310
      });
    }
  }

  $window.scroll(function () {
    if (window.innerHeight + document.body.scrollTop >= $window.height() && $infiniteScroll.length && page < $maxPages) {
      ajaxGetPageImages();
    }
  });

  function ajaxGetPageImages() {
    page++;
    $.get({
      url: '',
      data: 'page=' + page
    })
    .done(function(data) {
      $container.append(data);
      $container.imagesLoaded().progress(onProgress);
      imageCount = $container.find('img').length;
      loadedImageCount = 0;
    });
  }

  function onProgress(imgLoad, image) {
    loadedImageCount++;
    if (loadedImageCount == imageCount) {
      gridInit();
    }
  }

})
.define('app.pop-over', ['jQuery', 'docReady'], function () {

  $("#popover-cart").popover({
    html: true,
    toggle: 'popover',
    container: 'body',
    placement: 'top',
    trigger: 'focus',
    html: true,
    content: function() {
      return $('#popover-cart-content').html();
    }
  });

  $("#popover-info").popover({
    html: true,
    toggle: 'popover',
    container: 'body',
    placement: 'top',
    trigger: 'focus',
    html: true,
    content: function() {
      return $('#popover-info-content').html();
    }
  });

  var clipboard = new Clipboard('.popover-list__btn--share');
  $("#popover-share").popover({
    html: true,
    toggle: 'popover',
    container: 'body',
    placement: 'top',
    trigger: 'focus',
    html: true,
    content: function() {
      return $('#popover-share-content').html();
    }
  });

  $("#popover-add").popover({
    html: true,
    toggle: 'popover',
    container: 'body',
    placement: 'top',
    trigger: 'focus',
    html: true,
    content: function() {
      return $('#popover-add-content').html();
    }
  });

})
.define('app.fav', ['jQuery', 'docReady'], function () {

  favBtn = '.grid__fav';

  $(document).on('click', favBtn, function() {
    postFav($(this));
  });

  function postFav($this) {
    if (! $this.hasClass('active')) {
      $.post('/ajax/record/fav/', {
        action: 'add',
        record_id: $this.attr('data-record-id')
      })
      .done(function(){
        $('.grid__fav[data-record-id="' + $this.attr('data-record-id') + '"]').addClass('active');
      });
    }
    else {
      $.post('/ajax/record/fav/', {
        action: 'remove',
        record_id: $this.attr('data-record-id')
      })
      .done(function(){
        $('.grid__fav[data-record-id="' + $this.attr('data-record-id') + '"]').removeClass('active');
      });
    }
  }

})
.define('app.crop', ['jQuery', 'docReady'], function () {

  var $btn = $('.popover-list__btn');
  var $collection;
  var Cropper = window.Cropper;
  var submit;
  var target;
  var url;
  var image;
  var cropper;
  var aspectRatio;
  var recordId;
  var options = {
    aspectRatio: '',
    checkCrossOrigin: false,
    checkOrientation: false,
    movable: false,
    rotatable: false,
    scalable: false,
    zoomable: false,
    autoCropArea: 1,
    viewMode: 1
  }

  function cropperInit() {
    cropper = new Cropper(image, options);
  }

  $(document).ready(function() {

    // if order preview image found in document, initialize a cropper
    var orderPreviewImage = document.getElementById('order-preview__image');
    if (orderPreviewImage) {

      function productSettingsExistInForm () {
        if ($("input[name='crop_x']").val() === "None") return false;
        if ($("input[name='crop_y']").val() === "None") return false;
        if ($("input[name='crop_width']").val() === "None") return false;
        if ($("input[name='crop_height']").val() === "None") return false;
        return true;
      } 

      function setCropCoordinatesToFormFields () {
        var imageData = cropper.getImageData();
        var boxData = cropper.getCropBoxData();
        $("input[name='crop_x']").val(boxData.left);
        $("input[name='crop_y']").val(boxData.top);
        $("input[name='crop_width']").val(boxData.width);
        $("input[name='crop_height']").val(boxData.height);
        $("input[name='original_width']").val(imageData.width);
        $("input[name='original_height']").val(imageData.height);
      }

      function calculateNewPrice () {
        var amount = $('input[id="id_order-product-form-amount"]').val();
        var unitPrice = $('input[name=product]:checked').attr('data-price');
        var newPrice = parseInt(unitPrice) * parseInt(amount);
        $('#price-indicator').text(typeof newPrice !== 'number' || isNaN(newPrice) ? '?' : newPrice.toFixed(2));
        console.log('calculate new price for UI');
      }

      function isEmpty(obj) {
        for (var key in obj) {
          if (obj.hasOwnProperty(key)) return false;
        }
        return true;
      }

      function calculatePPI () {
        var $ppiIndicator = $('#ppi-indicator');
        var fullX = $ppiIndicator.attr('data-full-x');
        var fullY = $ppiIndicator.attr('data-full-y');
        var $inputChecked = $('input[name=product]:checked');
        var xInches = parseInt($inputChecked.attr('data-xsize')) / 25.4; // mm to in
        var yInches = parseInt($inputChecked.attr('data-ysize')) / 25.4;

        var imageArea = cropper.getImageData();
        console.log(imageArea)
        var cropArea = cropper.getCropBoxData();
        console.log(cropArea)
        var widthMultiplier = parseFloat(fullX) / imageArea.width;
        var heightMultiplier = parseFloat(fullY) / imageArea.height;

        var finalWidth = cropArea.width * widthMultiplier;
        var finalHeight = cropArea.height * heightMultiplier;

        var $PPIBox = $('#ppi-box');
        var PPI = Math.sqrt(Math.pow(finalWidth, 2) + Math.pow(finalHeight, 2)) / 
          Math.sqrt(Math.pow(xInches, 2) + Math.pow(yInches, 2));

      
        if (isNaN(PPI)) {
          $('#ppi-indicator').text('?');
        } else {
          if (PPI < 200 && !$PPIBox.hasClass('alert-danger')) $PPIBox.addClass('alert-danger');
          if (PPI >= 200 && $PPIBox.hasClass('alert-danger')) $PPIBox.removeClass('alert-danger');
          $('#ppi-indicator').text(Math.round(PPI));
        }

      }

      url = orderPreviewImage.getAttribute('data-img-url');
      image = orderPreviewImage;
      image.src=url;
      var aspectLandscape = 1.414;
      var aspectPortrait = 0.707;


      var savedAspectRatio = $("input[name='crop_width']").val() / 
        $("input[name='crop_height']").val();
      options.aspectRatio = savedAspectRatio ? savedAspectRatio: aspectLandscape;
      cropperInit();
     

      // whenever print product type is reselected, change form values and show in UI
      $('.ordertype').click(function() {
          console.log(this);
          options.aspectRatio = this.getAttribute('data-xsize') / this.getAttribute('data-ysize');
          console.log('aspect ratio changed');
          // Restart
          cropper.destroy();
          cropper = new Cropper(image, options);

          calculateNewPrice();
          calculatePPI();
          setCropCoordinatesToFormFields();
      }); 

      // why not work LöL
      var amountField = document.querySelector('#id_order-product-form-amount');
      amountField.addEventListener('input', function() {
        calculateNewPrice();
      });

     $(document).on('cropmove', function (e) {
        console.log('cropping');
        setCropCoordinatesToFormFields();
        calculatePPI();
        /* Prevent to start cropping, moving, etc if necessary
        if (e.action === 'crop') {
          e.preventDefault();
        }  */
      }); 

      window.onresize = function () {
        console.log('canvas area resizing...');
        var imageData = cropper.getImageData();
        var boxData = cropper.getCropBoxData();  
        setCropCoordinatesToFormFields();
        /* Prevent to start cropping, moving, etc if necessary
        if (e.action === 'crop') {
          e.preventDefault();
        } */
      };

      // need to wait until cropper is completely built to calculate PPI value and set cropper coordinates
      // to match order specs
      $(document).on('ready', function(e) {

        if (productSettingsExistInForm()) {
          console.log('settings exist');
          cropper.setCropBoxData({
            left: parseInt($("input[name='crop_x']").val()),
            top: parseInt($("input[name='crop_y']").val()),
            width: parseInt($("input[name='crop_width']").val()),
            height: parseInt($("input[name='crop_height']").val()),
          });
          console.log(cropper.getCropBoxData());
        } 
        if (!productSettingsExistInForm()) {
          console.log('settings dont exist');
          setCropCoordinatesToFormFields();
        }

        calculatePPI();  
      });
      
    }
  });
  

  // modal related cropper stuff begins here

  $('.my-modal--crop').on('shown.bs.modal', function() {
    if (image.complete && image.naturalHeight !== 0) {
      cropperInit();
    }
    else {
      image.addEventListener('load', cropperInit);
    }
  });
  $('.my-modal--crop').on('hidden.bs.modal', function() {
    cropper.destroy();
  });

  $(document).on('click', '.popover-list__btn--crop', function() {
    target = document.getElementById(this.getAttribute('data-target').substring(1));
    url = this.getAttribute('data-img-url');
    recordId = this.getAttribute('data-record-id')
    image = target.getElementsByClassName('crop__image')[0];
    image.src = url;
  });

  $('.crop__submit').on('click', function() {
    var $action = $(this).val();
    if ($action == 'add') {
      $action = $('input[name=collection]:checked').attr('data-action');
    }
    var $collectionTitle = $('#add-collection-input').val();
    var $collectionId = $('input[name=collection]:checked').val();
    var imageData = cropper.getImageData();
    var boxData = cropper.getCropBoxData();
    $.post('/ajax/crop/', {
      action: $action,
      x: boxData.left,
      y: boxData.top,
      width: boxData.width,
      height: boxData.height,
      original_width: imageData.width,
      original_height: imageData.height,
      collection_id: $collectionId,
      collection_title: $collectionTitle,
      record_id: recordId,
    })
    .done(function(data){
      if (data.url) {
        window.open(data.url, '_self');
      }
      else {
        location.reload();
      }
    })
    .fail(function(data){
      alert('Crop failed.');
    });
  });

  $(document).on('change', '.docs-toggles', function(event) {
    var e = event || window.event;
    var target = e.target || e.srcElement;
    var cropBoxData;
    var canvasData;
    var isCheckbox;
    var isRadio;

    if (!cropper) {
      return;
    }

    if (target.tagName.toLowerCase() === 'label') {
      target = target.querySelector('input');
    }

    isCheckbox = target.type === 'checkbox';
    isRadio = target.type === 'radio';

    if (isCheckbox || isRadio) {
      if (isCheckbox) {
        options[target.name] = target.checked;
        cropBoxData = cropper.getCropBoxData();
        canvasData = cropper.getCanvasData();

        options.ready = function () {
          cropper.setCropBoxData(cropBoxData).setCanvasData(canvasData);
        };
      } else {
        options[target.name] = target.value;
        options.ready = function () {
        };
      }

      // Restart
      cropper.destroy();
      cropper = new Cropper(image, options);
    }
  });

})
.define('app.editTitle', ['jQuery', 'docReady'], function () {

  $editBtn = $('#edit-title-btn');
  $editCancel = $('#edit-title-cancel');
  $removeItem = $('.grid__item-remove');
  $title = $('.banner__title');
  $description = $('.banner__description');
  $collectionForm = $('.banner__form');

  $removeItem.on('click', function() {
    var confirmRemove = confirm($(this).attr('data-confirm'));
    var $recordId = $(this).attr('data-record-id');
    if (confirmRemove) {
      $.post('', {
        action: 'remove-record',
        record_id: $recordId
      })
      .done(function() {
        location.reload();
      });
    }
  });

  $editCancel.on('click', function() {
    $title.toggle();
    $description.toggle();
    $collectionForm.toggle();
    $removeItem.toggle();
  });

  $editBtn.on('click', function() {
    $title.toggle();
    $description.toggle();
    $collectionForm.toggle();
    $removeItem.toggle();
  });

})
.define('app.zoom', ['jQuery', 'docReady'], function () {

  var img = document.getElementById('zoomable-image');

  if (!img) {
    return
  }

  if (img.complete && img.naturalHeight !== 0) {
    handleImageLoaded.call(img);
  }
  else {
    img.addEventListener('load', handleImageLoaded);
  }

  function handleImageLoaded() {
    var w = this.naturalWidth;
    var h = this.naturalHeight;
    var ar = w / h;
    var url = this.src;
    var fullResUrl = this.getAttribute('data-full-res-url');

    if ($(window).width() >= 1024) {
      h += $(window).height() * 2; // Picture initial size if scr width >=1024 px
      w = h * ar;
    }
    else if (w > h) {
      w += $(window).width() * 1.862; // Picture initial size if scr width < 1024 px & img width > img height
      h = w / ar;
    }
    else { // Picture initial size if scr width < 1024 px & img width <= img height
      h += $(window).height();
      w = h * ar;
    }

    zoomInit(w, h, url, fullResUrl);
  }

  function zoomInit(w, h, url, fullResUrl) {

    var imageContainer = L.map('zoomable-image-container', {
      center: [500, 500],
      minZoom: 1,
      maxZoom: 5,
      zoom: 2,
      crs: L.CRS.Simple,
      maxBoundsViscosity: 1,
      scrollWheelZoom: false
    });
    var bottomLeft = imageContainer.unproject([0, h], imageContainer.getMaxZoom()-1);
    var topRight = imageContainer.unproject([w, 0], imageContainer.getMaxZoom()-1);
    var bounds = new L.LatLngBounds(bottomLeft, topRight);
    var imagelayer = L.imageOverlay(url, bounds).addTo(imageContainer);
    var fullResLoaded = false;
    var $zoomInBtn = $('#zoom-in-btn');
    var $zoomOutBtn = $('#zoom-out-btn');

    imageContainer.setMaxBounds(bounds);

    imageContainer.on('zoomstart', function() {
      if (!fullResLoaded) {
        setTimeout(function() {
          L.imageOverlay(fullResUrl, bounds).addTo(imageContainer);
          img.addEventListener('load', function() {
            imagelayer.remove();
          });
          fullResLoaded = true;
        }, 300);
      }
    });

    $zoomInBtn.on('click', function() {
      imageContainer.zoomIn();
    });
    $zoomOutBtn.on('click', function() {
      imageContainer.zoomOut();
    });

  }


});
