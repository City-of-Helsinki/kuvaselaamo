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
.define('app.grid', ['jQuery', 'docReady', 'winReady'], function () {

  var $window = $(window);
  var $container = $('.flex-images');
  var $infiniteScroll = $('.flex-images.infinite-scroll');
  var $itemGroup = $('.grid__group');
  var $items = $('.flex-images .item');
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
    $container.flexImages({
      rowHeight: 200
    });
  }

  $window.scroll(function () {
    if (window.innerHeight + document.body.scrollTop >= $window.height() && $infiniteScroll.length) {
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

  favBtn = 'button.grid__fav';

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
        $this.addClass('active')
      });
    }
    else {
      $.post('/ajax/record/fav/', {
        action: 'remove',
        record_id: $this.attr('data-record-id')
      })
      .done(function(){
        $this.removeClass('active')
      });
    }
  }

})
.define('app.crop', ['jQuery', 'docReady'], function () {

  var $btn = $('.popover-list__btn');
  var $action;
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

  $(document).on('click', '.popover-list__btn', function() {
    target = document.getElementById(this.getAttribute('data-target').substring(1));
    url = this.getAttribute('data-img-url');
    recordId = this.getAttribute('data-record-id')
    image = target.getElementsByClassName('crop__image')[0];
    image.src = url;
    setTimeout(function() {
      cropperInit();
    }, 200);
  });

  $(document).on('click', '.crop-settings__toggle', function() {
    $('.crop-settings__form').collapse('toggle');
    if ($('#crop-add-submit').val() == 'add') {
      $('#crop-add-submit').val('add-create-collection');
    }
    else if ($('#crop-add-submit').val() == 'add-create-collection') {
      $('#crop-add-submit').val('add');
    }
  });

  $('.my-modal--crop').on('hidden.bs.modal', function() {
    cropper.destroy();
  });

  $('.crop__submit').on('click', function() {
    $action = $(this).val();
    $collectionId = $('input[name=collection]:checked').val();
    $collectionTitle = $('#add-collection-input').val();
    imageData = cropper.getImageData();
    boxData = cropper.getCropBoxData();
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
        window.open(data.url);
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
  $titleForm = $('.banner__title-form');

  $removeItem.on('click', function() {
    $recordId = $(this).attr('data-record-id');
    $.post('', {
      action: 'remove-record',
      record_id: $recordId
    })
    .done(function() {
      location.reload();
    });
  });

  $editCancel.on('click', function() {
    $title.toggle();
    $titleForm.toggle();
  });

  $editBtn.on('click', function() {
    $title.toggle();
    $titleForm.toggle();
  });

});
