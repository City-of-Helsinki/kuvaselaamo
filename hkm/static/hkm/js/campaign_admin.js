(function($) {
    $(document).ready(function() {
        var csrftoken = django.jQuery("[name=csrfmiddlewaretoken]").val();

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $("#generate-codes").on("click", function(e) {
            e.preventDefault();
            $.ajax({
                type: "POST",
                url: $(this).data("href"),
                data: {
                    amount: $("#id_amount").val(),
                    length: $("#id_length").val(),
                    prefix: $("#id_prefix").val()
                },
                success: function(response){
                    window.location.reload()
                }
            })

        });
    })
})(django.jQuery);