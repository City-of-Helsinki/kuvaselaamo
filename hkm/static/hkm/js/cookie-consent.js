(function($) {
    $(document).ready(function() {
        $("#cookie-consent").fadeIn();
        $( "#cookie-consent" ).animate({ "bottom": "0" }, "slow" );

        $("#cookie-consent__readmore-btn").click(function(){
            $("#cookie-consent__readmore-btn" ).hide();
            $("#cookie-consent__content" ).show();
        });

        $("#cookie-consent").click(function(){
            $("#cookie-consent__readmore-btn" ).hide();
            $("#cookie-consent__content" ).show();
        });
    });
    $(document).on('click', function (e) {
        if ($(e.target).closest("#cookie-consent").length === 0) {
            $("#cookie-consent__content").hide();
            $("#cookie-consent__readmore-btn" ).show();
        }
    });
})(jQuery);