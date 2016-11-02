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
        $(this).attr('data-w', w);
        $(this).attr('data-h', h);
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
    $.ajax({
      url: '',
      method: 'GET',
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

  // $.ajax({
  //   url: '',
  //   method: 'GET',
  //   data:
  // })
  // .done(function(data) {
  // });

});
