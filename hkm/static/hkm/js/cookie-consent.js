(function($) {
    var cookieName = "hki_consent"
    var cookie = $.cookie(cookieName)
    var _paq = window._paq = window._paq || [];

    if(!cookie && _paq) {
        _paq.push(['requireCookieConsent']);

        $("#cookie-consent").fadeIn();
        $( "#cookie-consent" ).animate({ "bottom": "0" }, "slow" );

        $("#cookie-consent__readmore-btn").on('click', function (e) {
            $("#cookie-consent__readmore-btn" ).hide();
            $("#cookie-consent__content" ).show();
        });

        $("#cookie-consent").on('click', function (e) {
            $("#cookie-consent__readmore-btn" ).hide();
            $("#cookie-consent__content" ).show();
        });
    }

    $("#consent_accept").on('click', function (e) {
        if(_paq) {
            _paq.push(['setCookieConsentGiven']);
            $.cookie(cookieName, 1, { expires : 393 });
            $("#cookie-consent").fadeOut();
        }
    });
        
    $("#consent_reject").on('click', function (e) {
        if(_paq) {
            _paq.push(['forgetCookieConsentGiven']);
            $.cookie(cookieName, 0, { expires : 393 });
            $("#cookie-consent").fadeOut();
        }
    });

    // click outside to collapse cookie consent
    $(document).on('click', function (e) {
        if ($(e.target).closest("#cookie-consent").length === 0) {
            $("#cookie-consent__content").hide();
            $("#cookie-consent__readmore-btn" ).show();
        }
    });
})(jQuery);