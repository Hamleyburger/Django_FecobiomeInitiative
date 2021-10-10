
// Submit post on submit
$('#newsletter-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    subscribe_newsletter();
});

// AJAX for posting
function subscribe_newsletter() {
    console.log("subscribe newsletter is working!") // sanity check
    console.log($('#input-email').val())
    subscribtion_url = $('#subscribe-newsletter-btn').data('url');
    
    $.ajax({
        url : subscribtion_url, // the endpoint
        type : "POST", // http method
        data : { input_email : $('#input-email').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            if (json.error) {
                console.log("error");
            }
            if (json.success) {
                console.log("success");
                $('#input-email').val(''); // remove the value from the input
                // show-slode-message: show a message and slide it up
                $('#ajax-message-content').html("Successfully subscribed to the Fecobiome Initiative newsletter");
                $("#ajax-message").fadeTo(6000, 500).slideUp(500, function() {
                    $("#ajax-message").slideUp(500);
                });
                // end of show-slide-message function
            }
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};




// Submit post on submit
$('#membership-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    request_membership();
});

// AJAX for posting
function request_membership() {
    console.log("request membership is working!") // sanity check
    console.log($('#id-email').val())
    console.log($('#id-firstname').val())
    console.log($('#id-lastname').val())
    console.log($('#id_profile_picture').val())
    console.log($('#id_display_member').val())
    subscribtion_url = $('#register-member-btn').data('url');
    
    $.ajax({
        url : subscribtion_url, // the endpoint
        type : "POST", // http method
        data : { input_email : $('#input-email').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            if (json.error) {
                console.log("error");
            }
            if (json.success) {
                console.log("success");
                $('#input-email').val(''); // remove the value from the input
                // show-slode-message: show a message and slide it up
                $('#ajax-message-content').html("Successfully subscribed to the Fecobiome Initiative newsletter");
                $("#ajax-message").fadeTo(6000, 500).slideUp(500, function() {
                    $("#ajax-message").slideUp(500);
                });
                // end of show-slide-message function
            }
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};





// Someone else's code to get csrf token
$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});