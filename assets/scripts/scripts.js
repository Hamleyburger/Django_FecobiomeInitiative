// Make navbar toggle the "scrolled" class when being at scroll position past hero title
 $(window).scroll(function(){
    const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
    // to find distance to title
    var title_position = $(".hero-title").position();
    //console.log(title_position);
 $('.nav-panel').toggleClass('scrolled', $(this).scrollTop() > title_position.top-60);
 });



$(document).ready(function() {
    // When element navbar-collapse has class "collapsing", toggle class "clicked" in nav-panel
    $(".navbar-toggler").click(function () {
        // Super hackish function to detect whether navbar is growing or shrinking to try to 
        // determine whether a click should trigger a solid background color or transparency
        let firstmeasure;
        let secondmeasure;
        firstmeasure = $(".nav-panel").height()
        setTimeout(function(){
            secondmeasure = $(".nav-panel").height()
            if (firstmeasure < secondmeasure) {
                $(".nav-panel").addClass("expanded");
            }
            else {
                $(".nav-panel").removeClass("expanded");
            }
        }, 60); // milliseconds. Can still fail if the navbar is both shrinking and growing within the time interval
    });
    
});

$(document).ready(function() {
    var m = $(".django-alert");
    $(m).fadeTo(6000, 500).slideUp(500, function() {
        console.log("doing something");
        $(m).slideUp(500);
    });
});


// Creates a new message element and fades it out. Destroys the previous if any.
function flash_message_with_ajax(message, alert_class) {
    console.log("flashing");

    $("#ajax-message").remove();

    jQuery('<div>', {
        id: 'ajax-message',
        style: '',
        class: 'container-fluid p-0',
    }).appendTo('.feedback-messages');

    jQuery('<div>', {
        id: 'ajax-message-class',
        style: '',
        class: 'alert fade show',
        role: "alert",
    }).appendTo('#ajax-message');

    jQuery('<span>', {
        id: 'ajax-message-content',
    }).appendTo('#ajax-message-class');

    // show-slide-message: show a message and slide it up
    $('#ajax-message-content').html(message);
    $('#ajax-message-class').removeClass("alert-danger");
    $('#ajax-message-class').removeClass("alert-success");
    $('#ajax-message-class').addClass(alert_class);
    $("#ajax-message").fadeTo(6000, 500).slideUp(500, function() {
        $("#ajax-message").slideUp(500);
    });
    // end of show-slide-message function
    
}