palikka
.define(['jQuery'], function () {

  return window[this.id];

})
.define('docReady', ['jQuery'], function ($) {

  return palikka.defer($);

})
.define('app.muuri', ['jQuery', 'docReady'], function ($) {

  var grid = new Muuri({
    container: document.getElementsByClassName('muuri-grid')[0],
    items: document.getElementsByClassName('muuri-item')
  });

});
