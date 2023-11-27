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

  // always require on load
  _paq.push(["requireCookieConsent"]);
  _paq.push(["requireConsent"]);

  // if rejected
  if (cookie && cookie === 0) {
    _paq.push(["forgetCookieConsentGiven"]);
    _paq.push(["forgetConsentGiven"]);
  }

  // if accepted
  if (cookie && cookie === 1) {
    _paq.push(["rememberConsentGiven"]);
    _paq.push(["rememberCookieConsentGiven"]);
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
      _paq.push(["rememberConsentGiven"]);
      _paq.push(["rememberCookieConsentGiven"]);
      $.cookie(cookieName, 1, { expires: 393 });
      $cookieConsentContainer.fadeOut();
    }
  });

  $rejectBtn.on("click", function (e) {
    if (_paq) {
      _paq.push(["forgetConsentGiven"]);
      _paq.push(["forgetCookieConsentGiven"]);
      $.cookie(cookieName, 0, { expires: 393 });
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
