$(document).ready(function() {
    // Basket page add remove quantity

    function getValues(selector) {
      var count = parseInt(selector.closest('.basket-row').find('.basket-quantity-value').text(), 10);

      return {
          count: count
      }
    }

    // Handles the click events
    function handleCount(e) {
      e.preventDefault();
      var currentCount = getValues($(this)).count;

      if ($(this).hasClass('btn-up')) {
        currentCount += 1;
      }
      else {
        if (currentCount > 1) {
            currentCount -= 1;
        }
      }
        $.ajax({
            type: "POST",
            url: "",
            data: {
                "action": "update",
                "quantity": currentCount,
                "line": $(this).closest('.basket-row').data("lineid")
            },
            success: function (data) {
                $(".container-center").html(data.html);
                $(".product-counter").html(data.nav_counter);

            }
        })
    }

    function handleDelete(e){
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "",
            data: {
                "action": "delete",
                "line": $(this).closest('.basket-row').data("lineid")
            },
            success: function (data) {
                $(".container-center").html(data.html);
                $(".product-counter").html(data.nav_counter);
            }
        })
    }

    // Bind click event to buttons
    $('body').on('click', '.btn-up, .btn-down', handleCount);
    $('body').on('click', '.btn-delete-row', handleDelete);
    // Init tooltips
    $(document.body).tooltip({ selector: "[title]" });
});
