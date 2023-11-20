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

  // Hide login modal if user wants to reset password.
  $('#reset-pwd-btn').on('click', hideModal);

  // Hide password reset modal if user is navigating back to log in.
  $('#back-to-login-btn').on('click', hideModal);

  // In addition to hiding the modal, hide the bottom green search modal
  // and make more space for signup to expand

  $('#signup-btn').on('click', function() {
    hideModal();
    hideSearchModal();
  });

  $('#account-dropdown').on('click', hideModal);
  $('#nav-collapse-btn').on('click', hideModal);

  $('#landing-search-close').on('click', hideSearchModal);
  $('.actions').on('click', hideSearchModal);
  $('#zoomable-image-container').on('click', hideSearchModal);

  function hideModal() {
    $('.modal').each(function() {
      if ($(this).hasClass('in')) {
        $(this).modal('hide');
      }
    });
  }

  // Close the search modal function whenever called

  function hideSearchModal() {
    $('#landing-search').fadeOut();
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
.define('app.search-form', ['jQuery', 'docReady'], function () {
  const formErrorMessage = $('.search-form-message');
  const urlParams = new URLSearchParams();

  $('#search-form').on('submit', function(event) {
    event.preventDefault();

    const formValues = $(this).serializeArray();

    // Use only the following fields for url params
    const urlParamFields = ['search', 'date_from', 'date_to'];

    formValues.forEach(formVal => {
      if (formVal.value && urlParamFields.includes(formVal.name)) {
        // Add to url params
        urlParams.set(formVal.name, formVal.value);
      }
    });

    const date_from = formValues.find(fv => fv.name === "date_from")?.value ?? 0;
    const date_to = formValues.find(fv => fv.name === "date_to")?.value ?? 0;

    // Do not allow date_from being larger / after date_to. Show message instead.
    if (date_from > 0 && date_to > 0 && Number(date_from) > Number(date_to)) {
      $(formErrorMessage).removeClass('hidden');
    }
    else {
      // Delete "page" parameter to make sure everything is in sync
      urlParams.delete("page")

      window.open('?' + urlParams.toString(), '_self');
    }

  });
})
.define('app.search-filter', ['jQuery', 'docReady'], function () {
  var $filterLink = $('.facet-filter');
  var $deleteBtns = $('.search-filter__delete');
  const urlParams = new URLSearchParams(window.location.search)

  $filterLink.on('change', function() {
    const facetName = $(this).attr('data-facet-type');
    const facetValue = $(this).val();

    if (!facetValue) {
      return;
    }

    // Allow only one date range selection for now
    if (facetName === "date_from" || facetName === "date_to") {
      urlParams.set(facetName, facetValue)
    }
    else {
      urlParams.append(facetName, facetValue)
    }

    // Delete "page" parameter to make sure everything is in sync
    urlParams.delete("page")

    window.open('?' + urlParams.toString(), '_self');
  });

  $deleteBtns.on('click', function() {
    const facetName = $(this).attr('data-facet-type');
    const facetValue = $(this).attr('data-facet-value');

    if (facetName === "date_range") {
      urlParams.delete('date_from');
      urlParams.delete('date_to');
    }
    const values = urlParams.getAll(facetName)

    if (Array.isArray(values)) {
      const index = values.indexOf(facetValue);

      values.splice(index, 1);

      if (values.length === 0) {
        urlParams.delete(facetName);
      } else {
        // Delete all values from to object
        urlParams.delete(facetName);
        // Construct key value pairs again, this results url params being in a "correct" format
        // E.g date=1940&date=1950 instead of date=1940,1950
        values.forEach(val => {
          urlParams.append(facetName, val)
        });
      }
    }
    // Delete "page" parameter to make sure everything is in sync
    urlParams.delete("page")

    window.open('?' + urlParams.toString(), '_self');
  });
})
.define('app.grid', ['jQuery', 'docReady', 'winReady'], function () {

  var $window = $(window);
  var $container = $('.flex-images');
  var $infiniteScroll = $('.flex-images.infinite-scroll');
  var $itemGroup = $('.grid__group');
  var $items = $('.flex-images .item');
  var $maxPages = $('.grid').attr('data-pages');
  var loadMoreButton = $('#btn-load-more');
  var page = 1;
  var loadedImageCount = 0;
  var imageCount = 40;
  var fetchingMoreImages = false;
  var queryParameters = {};
  var queryString = location.search.substring(1);

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
    scrollToLastItem();
  }

  function scrollToLastItem() {

    var itemId = localStorage.getItem("last_record_browsed") || "_";
    // Remove white spaces in case of multiple search keywords
    itemId = itemId.replace(' ', '_');
    var $item = $("[name="+itemId+"]");
    if($item.length) {
      $('html, body').animate({
        scrollTop: $item.offset().top
      }, 1000);
      localStorage.setItem("last_record_browsed", "");
    }
  }

  // Make ajax calls to the api server on button click

  loadMoreButton.on('click', function() {
    fetchingMoreImages = true;
    var page = parseInt($(this).data("current-page")) || 0;
    ajaxGetPageImages(page+1);
    // if ( !$(this).has('.icon-spinner') ) {
    //   $(this).append($('<i class="icon-spinner"></i>'));
    // }
    $(this).append($('<i class="icon-spinner"></i>'));
  });

  function ajaxGetPageImages(page) {
    $.get({
      url: '',
      data: 'loadallpages=0&page=' + page
    })
    .done(function(data) {
      var re = /([^&=]+)=([^&]*)/g, m;

      while (m = re.exec(queryString)) {
        queryParameters[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
      }
      queryParameters['page'] = page;

      window.history.replaceState("", "", "?"+$.param(queryParameters));
      $container.append(data);
      $container.imagesLoaded().progress(onProgress);
      imageCount = $container.find('img').length;
      loadedImageCount = 0;
      fetchingMoreImages = false;
      loadMoreButton.find('.icon-spinner').remove();
      loadMoreButton.data({'current-page': page})
    })
    .fail(function(jqXHR, textStatus){
      loadMoreButton.attr("disabled", true);
      // translated button text is given in search.html template
      loadMoreButton.html(window.NO_MORE_SEARCH_RESULTS_TEXT);
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
    container: '.actions',
    placement: 'top',
    trigger: 'click',
    html: true,
    content: function() {
      return $('#popover-cart-content').html();
    }
  });

  $("#popover-share").popover({
    html: true,
    toggle: 'popover',
    container: '.actions',
    placement: 'top',
    trigger: 'click',
    content: function() {
      return $('#popover-share-content').html();
    }
  });
  
  $("#popover-share").click(function(evt) {
    evt.stopPropagation();
  });

  $('html').click(function() {
      $('#popover-share').popover('hide');
  });

  $("#popover-cart").click(function(evt) {
    evt.stopPropagation();
  });

  $('html').click(function() {
      $('#popover-cart').popover('hide');
  });

  $('body').on('click', 'a.share-item', function(e) {
    e.preventDefault();
    var href = window.location.href;
    var title = encodeURIComponent($('.record-meta__title').text());
    var imageUrl = encodeURIComponent($('#zoomable-image').attr('src'));
    var windowTitle = '';
    var sharerBaseUrl = '';
    var sharerParams = '';

    if($(this).hasClass('share-fb')) {
      sharerBaseUrl = 'https://www.facebook.com/sharer/sharer.php';
      windowTitle = 'Facebook - ' + title;
      sharerParams = '?u=' + href + '&p[images][0]=' + imageUrl;
    } else if($(this).hasClass('share-tw')) {
      sharerBaseUrl = 'https://twitter.com/share';
      windowTitle = 'Twitter - ' + title;
      sharerParams = '?url=' + href;
    } else if($(this).hasClass('share-pin')) {
      sharerBaseUrl = 'http://pinterest.com/pin/create/button/';
      windowTitle = 'Pinterest -';
      sharerParams = '?url=' + href;
      // sharerParams = '?url=' + href + '&media=' + imageUrl + '&description=' + title;
    }
    openWindow(window, sharerBaseUrl + sharerParams, windowTitle);
  });

  // share social opener

  // https://github.com/nygardk/react-share/blob/29fa4b957e0ebc7e089207cbc5b07c373c6fb4e0/src/ShareButton.tsx#L11
  function getBoxPositionOnWindowCenter(window, height, width) {
    return {
      left:
      window.outerWidth / 2 +
      (window.screenX || window.screenLeft || 0) -
      width / 2,
      top:
        window.outerHeight / 2 +
        (window.screenY || window.screenTop || 0) -
        height / 2,
    }
  };

  function openWindow(window, href, name) {
    const height = 400;
    const width = 550;
    const { left, top } = getBoxPositionOnWindowCenter(window, width, height);
    // https://github.com/nygardk/react-share/blob/29fa4b957e0ebc7e089207cbc5b07c373c6fb4e0/src/ShareButton.tsx#L26
    const config = {
      centerscreen: 'yes',
      chrome: 'yes',
      directories: 'no',
      height,
      left,
      location: 'no',
      menubar: 'no',
      resizable: 'no',
      scrollbars: 'yes',
      status: 'no',
      toolbar: 'no',
      top,
      width,
    };
    // A comma separated list of key value pairs without whitespace.
    // E.g. height=400,width=400
    const windowFeatures = Object.entries(config)
      .map(([key, value]) => `${key}=${value}`)
      .join(',');
  
    window.open(href, name, windowFeatures);
  }

  // scroll down to detail section when info button clicked
  $("#actions-info").click(function(){
    $("html, body").animate({
      scrollTop: $("#detail-section").offset().top
    }, 500);
  })

  var clipboard = new Clipboard('#actions-share');

  $('.has-popover').on('click', function() {
      var clickedButton = this;
      $('.has-popover').each(function(current) {
        if ($(this)[0] !== clickedButton) {
          $(this).popover('hide').tooltip('hide');
        }
        else {
          $(this).popover('toggle');
        }
      });
      $(this).tooltip('hide');
  });

  $('.actions__btn').each(function(){
    $(this).tooltip({
      title: $(this).attr("tooltip-title")
    })
  });
})
.define('app.fav', ['jQuery', 'docReady'], function () {

  favBtn = '.grid__fav';
  navFavBtn = '.nav__fav';

  $(document).on('click', favBtn, function() {
    postFav($(this), favBtn);
  });

  $(document).on('click', navFavBtn, function() {
    console.log('nav fav button clicked');
    postFav($(this), navFavBtn);
  });

  function postFav($this, favClass) {
    if (! $this.hasClass('active')) {
      $.post('/ajax/record/fav/', {
        action: 'add',
        record_id: $this.attr('data-record-id')
      })
      .done(function(){
        $(favClass + '[data-record-id="' + $this.attr('data-record-id') + '"]').addClass('active');
      });
    }
    else {
      $.post('/ajax/record/fav/', {
        action: 'remove',
        record_id: $this.attr('data-record-id')
      })
      .done(function(){
        $(favClass + '[data-record-id="' + $this.attr('data-record-id') + '"]').removeClass('active');
      });
    }
  }
})
.define('app.reset-password', ['jQuery', 'docReady'], function() {
  $('#password-reset-email').on('submit', function(event) {
    event.preventDefault();

    $.post('/', {
      action: 'password_reset',
      csrfmiddlewaretoken: event.target.elements.csrfmiddlewaretoken.value,
      email: event.target.elements.email.value,
    }).done(function () {
        $('#password-reset-form').addClass('hidden');
        $('#password-reset-response-success').removeClass('hidden');
        $('#password-reset-success-title').focus();
    }).fail(function () {
      $('#password-reset-form').addClass('hidden');
      $('#password-reset-response-error').removeClass('hidden');
      $('#password-reset-error-title').focus();
    })
  })

  // When user closes the modal after success message. Reset content to previos state.
  $('#password-reset').on('hidden.bs.modal', function () {
    $('#password-reset-form').removeClass('hidden');
    $('#password-reset-response-success').addClass('hidden');
  })

  // Logic for opening the password reset modal automatically
  const pathname = window.location.pathname;
  const showPasswordChangeModal = pathname.includes('reset');

  if (showPasswordChangeModal) {
    $('#password-change').modal('toggle')
  }

  // POST password reset form data
  $('#password-set-new').on('submit', function (event) {
    event.preventDefault();

    $.post(pathname, {
      csrfmiddlewaretoken: event.target.elements.csrfmiddlewaretoken.value,
      new_password1: event.target.elements.new_password1.value,
      new_password2: event.target.elements.new_password2.value
    }).done(function (response) {
      $('#password-set-form').addClass('hidden');
      $('#password-set-success').removeClass('hidden');
      $('#password-set-success-title').focus();

    }).fail(function (response) {
      // Remove old error
      $('#password-set-validation-error').remove()
      const error_message = response.responseJSON.error_message;
      $('#id_new_password2').after(`<div id="password-set-validation-error" class="login-modal__body_error">${error_message}</div>`)
      $('#password-set-error-title').focus();
    })
  })
})
.define('app.feedback', ['jQuery', 'docReady'], function() {
  $('#feedback-form').on('submit', function(event) {
    event.preventDefault();

    $.post('/record/feedback/', {
      action: 'feedback',
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
      content: $('#id_feedback-form-content').val(),
      full_name: $('#id_feedback-form-full_name').val(),
      email: $('#id_feedback-form-email').val(),
      hkm_id: $('input[name="hkm_id"]').val(),
    }).done(function(response) {
      if (response.result === "Success") {
        // Empty form fields
        $('#id_feedback-form-content').val('');
        $('#id_feedback-form-full_name').val('');
        $('#id_feedback-form-email').val('');
        // Uncover success message
        $("#fb-success").removeClass("hidden");
        $("#fb-error").addClass("hidden");
      }
    }).fail(function() {
      // Uncover error message
      $("#fb-error").removeClass("hidden");
      $("#fb-success").addClass("hidden");
    })
  })

})
.define('app.addToCollection', ['jQuery', 'docReady'], function() {
  $('#add-to-collection').on('click', function() {
    const action = $('input[name=collection]:checked').attr('data-action');
    const collectionTitle = $('#add-collection-input').val();
    const collectionId = $('input[name=collection]:checked').val();
    const recordId = this.getAttribute('data-record-id');

    $.post('/ajax/collection/', {
      action: action,
      collection_id: collectionId,
      collection_title: collectionTitle,
      record_id: recordId,
    })
      .done(function() {
        $('#collection-add').modal('hide');
    })
      .fail(function() {
        // At the moment there is no better way to display errors.
        alert('Add to collection failed.')
      })
  })
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

    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip({
      container: 'body'
    });

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

  $(document).on('click', '.actions_crop', function() {
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
        window.open(data.url);
        $('#crop-dl').remove();
        $('.my-modal--crop').modal('hide');
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


    if (window.innerWidth > window.innerHeight) {
      if (w > h) {
        w = window.innerWidth * ar;
        h = w / ar;
      }
      else {
        h = window.innerHeight / ar * 1.2;
        w = h * ar;
      }
    }
    else {
    }
    zoomInit(w, h, url, fullResUrl);
  }

  function zoomInit(w, h, url, fullResUrl) {
    // debugger;

    var initialZoom = 3;

    var imageContainer = L.map('zoomable-image-container', {
      center: [500, 500],
      minZoom: 1,
      maxZoom: 5,
      zoom: initialZoom,
      crs: L.CRS.Simple,
      maxBoundsViscosity: 1,
      scrollWheelZoom: false,
      zoomControl: true
    });
    var bottomLeft = imageContainer.unproject([0, h], imageContainer.getMaxZoom()-1);
    var topRight = imageContainer.unproject([w, 0], imageContainer.getMaxZoom()-1);
    var bounds = new L.LatLngBounds(bottomLeft, topRight);
    var imagelayer = L.imageOverlay(url, bounds).addTo(imageContainer);
    var fullResLoaded = false;
    var $zoomInBtn = $('#zoom-in-btn');
    var $zoomOutBtn = $('#zoom-out-btn');
    var $image = $('#zoomable-image-container');
    var zoomable = true;
    var clickedAt;

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

    // image can be zoomed with buttons and with left and right mouse clicks. image can be moved by click-dragginw with mouse
    $zoomInBtn.on('click', function() {
      imageContainer.zoomIn();
    });
    $zoomOutBtn.on('click', function() {
      imageContainer.zoomOut();
    });


    $image.on('mousedown', function(e) {

      clickedAt = new Date().getTime();
    });
    // on mouseup, zoom if permitted
   $image.on('mouseup', function(e) {

      var mouseUpAt = new Date().getTime();
      if (zoomable && mouseUpAt - clickedAt < 300) {
        switch(e.which) {
          case 1:
            console.log('left mouse button');
            imageContainer.zoomIn();
            break;
          case 3:
            imageContainer.zoomOut();
            console.log('right mouse button');
            break;
          default:
            break;
        }
      }
    });

   imageContainer.on('movestart', function() {
      zoomable = false;
   });
   imageContainer.on('moveend', function() {
      zoomable = true;
   });

    // prevent right click menu
    $image.on('contextmenu', function(e) {
      e.preventDefault();
    });



  }
});
