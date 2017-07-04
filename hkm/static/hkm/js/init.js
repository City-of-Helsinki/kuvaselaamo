(function($) {
    $(document).ready(function() {
        CKEDITOR.replace('id_content', {
            extraAllowedContent: '*(*)',
            contentsCss: '/static/hkm/css/main.css'
        });
    });
})(django.jQuery);
