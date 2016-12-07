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
    autoCropArea: 1
  }

  function cropperInit() {
    cropper = new Cropper(image, options);
  }

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
    var url = this.src;
    var fullResUrl = this.getAttribute('data-full-res-url');
    zoomInit(w, h, url, fullResUrl);
  }

  function zoomInit(w, h, url, fullResUrl) {

    var imageContainer = L.map('zoomable-image-container', {
      minZoom: 4,
      maxZoom: 6,
      center: [0, 0],
      zoom: 5,
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
