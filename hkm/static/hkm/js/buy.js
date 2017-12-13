$(document).ready(function() {

    function handleAddToBasket(e) {
        e.preventDefault();
        var orderUrl = $(this).data("action");
        $('html, body').css("cursor", "wait");
        $.ajax({
            url: orderUrl,
            method: "POST",
            data: {
                action: "order"
            },
            success: function(response) {
                if (response.redirect) {
                    location.href = response.redirect;
                }
            },
            error: function () {
                $('html, body').css("cursor", "auto");
            }
        });
    }


    $('body').on('click', '.grid__item--buy', handleAddToBasket);
});