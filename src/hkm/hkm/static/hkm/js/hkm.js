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
  var $items = $('.flex-images .item');
  var $status = $('#status');
  var $progress = $('progress');
  var page = 1;
  var loadedImageCount = 0;
  var imageCount;
  var supportsProgress = $progress[0] && $progress[0].toString().indexOf('Unknown') === -1;

  gridInit();

  $window.scroll(function () {
    if (window.innerHeight + document.body.scrollTop >= $window.height()){
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
    .done(function(page) {
      var images = $(page).find('.flex-images .item')
      $container.append(images);
      $container.imagesLoaded()
        .progress( onProgress )
        .always( onAlways );
      // reset progress counter
      imageCount = $container.find('img').length;
      loadedImageCount = 0;
    });
  }

  function gridInit() {
    $('.flex-images .item').each(function () {
      $(this).removeClass('hidden');
      var w = $(this).find('img').width();
      var h = $(this).find('img').height();
      $(this).attr('data-w', w);
      $(this).attr('data-h', h);
    });
    $container.flexImages({
      rowHeight: 200
    });
  }

  function updateProgress( value ) {
    if ( supportsProgress ) {
      $progress.attr( 'value', value );
    } else {
      // if you don't support progress elem
      $status.text( value + ' / ' + imageCount );
    }
    if (loadedImageCount == imageCount) {
      gridInit();
    }
  }

  // triggered after each item is loaded
  function onProgress( imgLoad, image ) {
    // change class if the image is loaded or broken
    var $item = $( image.img ).parent().parent();
    $item.addClass('is-loading');
    if ( !image.isLoaded ) {
      $item.addClass('is-broken');
    }
    // update progress element
    loadedImageCount++;
    updateProgress( loadedImageCount );
  }

  // hide status when done
  function onAlways() {
    $status.css({ opacity: 0 });
  }

})
.define('app.pop-over', ['jQuery', 'docReady'], function () {

  $('[data-toggle="popover"]').popover();

});
