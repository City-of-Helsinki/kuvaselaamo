palikka
.define(['jQuery'], function () {

  return window[this.id];

})
.define('docReady', ['jQuery'], function ($) {

  return palikka.defer($);

})
.define('app.grid', ['jQuery', 'docReady'], function ($) {

  $('.flex-images .item').each(function () {
    var w = $(this).find('img').width();
    var h = $(this).find('img').height();
    $(this).attr('data-w', w);
    $(this).attr('data-h', h);
  });

  $('.flex-images').flexImages({
    rowHeight: 200
  });

})
.define('app.pop-over', ['jQuery', 'docReady'], function ($) {

  $('[data-toggle="popover"]').popover();

});
