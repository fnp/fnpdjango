(function($) {
$(function() {

$("#annoy").each(function(i, annoy) {

    var edition = "annoyed" + new Date().getFullYear();

    var have_localstorage;
    try {
        localStorage.setItem("test", "test");
        localStorage.removeItem("test");
        have_localstorage = true;
    } catch(e) {
        have_localstorage = false;
    }

    $("#annoy-on").click(function(e) {
        e.preventDefault();
        $(annoy).slideDown('fast');
        $(this).hide();
        if (have_localstorage) localStorage.removeItem(edition);
    });

    $("#annoy-off").click(function() {
        $(annoy).slideUp('fast');
        $("#annoy-on").show();
        if (have_localstorage) localStorage[edition] = true;
    });

    if (have_localstorage) {
        if (!localStorage[edition]) {
            $("#annoy-on").hide();
            $(annoy).show();
        }
    }
    });


});
})(jQuery);
