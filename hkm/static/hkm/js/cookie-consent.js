(function ($) {
  var cookieName = "hki_consent";
  var cookie = $.cookie(cookieName);
  var _paq = (window._paq = window._paq || []);

  const $cookieConsentContainer = $("#cookie-consent"),
    $readMoreBtn = $("#cookie-consent__readmore-btn"),
    $cookieContents = $("#cookie-consent__content"),
    $acceptBtn = $("#consent_accept"),
    $rejectBtn = $("#consent_reject"),
    $consentLink = $("#cookie-consent-link");

  // if accepted
  if (cookie && cookie === "1") {
    _paq.push(['setCookieConsentGiven']);
  }

  if (!cookie) {
    $cookieConsentContainer.fadeIn();
    $cookieConsentContainer.animate({ bottom: "0" }, "slow");

    $readMoreBtn.on("click", function (e) {
      $readMoreBtn.hide();
      $cookieContents.show();
    });
  }

  $cookieConsentContainer.on("click", function (e) {
    $readMoreBtn.hide();
    $cookieContents.show();
  });

  $acceptBtn.on("click", function (e) {
    if (_paq) {
      _paq.push(['setCookieConsentGiven']);
      $.cookie(cookieName, "1", { expires: 393, path: '/' });
      $cookieConsentContainer.fadeOut();
    }
  });

  $rejectBtn.on("click", function (e) {
    if (_paq) {
      _paq.push(['forgetCookieConsentGiven']);
      $.cookie(cookieName, "0", { expires: 393, path: '/' });
      $cookieConsentContainer.fadeOut();
    }
  });

  // click cookie consent footer navi link to force open
  $consentLink.on("click", function (e) {
    e.preventDefault();
    $cookieConsentContainer.fadeIn();
    $cookieConsentContainer.animate({ bottom: "0" }, "slow");
    $cookieContents.show();
    $readMoreBtn.hide();
  });

  // click outside to collapse cookie consent
  $(document).on("click", function (e) {
    if ($(e.target).closest("#cookie-consent").length === 0) {
      $cookieContents.hide();
      $readMoreBtn.show();
    }
  });
})(jQuery);
