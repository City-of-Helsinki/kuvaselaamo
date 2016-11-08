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

  $btn = $('.popover-list__btn');
  var submit;

  $(document).on('click', '.popover-list__btn', function() {
    var target = document.getElementById(this.getAttribute('data-target').substring(1));
    var url = this.getAttribute('data-img-url');
    var image = target.getElementsByClassName('crop__image')[0];
    var imageContainer = target.getElementsByClassName('crop__container')[0];
    submit = target.getElementsByClassName('crop__submit')[0];
    image.src = url;
    setTimeout(function() {
      cropperInit(image, imageContainer);
    }, 200);
  });

  function cropperInit(image, imageContainer) {
    var Cropper = window.Cropper;
    var cropper = new Cropper(image, {
      // aspectRatio: 16 / 9,
      checkCrossOrigin: false,
      checkOrientation: false,
      // viewMode: 3,
      dragMode: 'move',
      autoCropArea: 1,
      crop: function(e) {
        // console.log(e.detail.x);
        // console.log(e.detail.y);
        // console.log(e.detail.width);
        // console.log(e.detail.height);
        // console.log(e.detail.rotate);
        // console.log(e.detail.scaleX);
        // console.log(e.detail.scaleY);
      }
    });
  }

    $(submit).on('click', function() {
      alert();
      imageData = cropper.getImageData();
      boxData = cropper.getCropBoxData();
      $.post('', {
        action: 'crop',
        x: boxData.left,
        y: boxData.top,
        width: boxData.width,
        height: boxData.height,
        original_width: imageData.width,
        original_height: imageData.height,
        record_id: $(image).attr('data-record-id')
      })
      .done(function(){
        alert('Image cropped!');
      });
    });



})
.define('app.editTitle', ['jQuery', 'docReady'], function () {

  $editBtn = $('#edit-title-btn');
  $title = $('.banner__title');
  $titleForm = $('.banner__title-form');

  $editBtn.on('click', function() {
    $title.toggle();
    $titleForm.toggle();
  });

});
