$(function () {

    $(".sidenav").sidenav();
    $('select').formSelect();

    $(document)
        .on('click', '.status-bar button', function (e) {
            $(this).closest('.status-bar').hide(200)
        })
        .on('click', '.copy', function () {
        var input = $(this).closest('.row').find('input').first();
        input.select();
        document.execCommand("copy");
        input.blur();
        Materialize.toast('Link copied to clipboard!', 2500)
    });

    $("a").on('click', function (event) {
        if (this.hash !== "" && $(this.hash).length) {
            event.preventDefault();
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 500, function () {
                //window.location.hash = hash;
            });
        }
    });
});
