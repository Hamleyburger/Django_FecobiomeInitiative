
// Submit post on submit
$('#newsletter-form').on('submit', function(event){
    event.preventDefault();
    subscribe_newsletter();
});

// AJAX for posting
function subscribe_newsletter() {
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
                flash_message_with_ajax("Successfully subscribed to the Fecobiome Initiative newsletter", "alert-success");
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






$('#membership-form').submit(function(event) { // catch the form's submit event
    event.preventDefault();
    form_action_url = $(this).attr('action');

    // Wrap the ajax call in recaptcha code to have Google generate a recaptcha token
    // Docs: https://developers.google.com/recaptcha/docs/v3
    grecaptcha.ready(function() {
        grecaptcha.execute(recaptcha_site_key, {action: 'submit'}).then(function(recaptcha_token) {

            fd = new FormData();
            if ($("#register-member-btn").hasClass("clicked")) {
                console.log("already clicked");
            }
            $(".loading-dots-toggle").toggle();
            $("#register-member-btn").addClass("clicked");
            
            // Get values
            // recaptcha_token is already = recaptcha_token
            csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]')[0].value;
            first_name = $("#id_first_name").val();
            last_name = $("#id_last_name").val();
            email = $("#id_email").val();
            affiliation = $("#id_affiliation").val();
            display_member = $("#id_display_member").val();
            
            if (cropped_blob != null) {
                profile_picture = new File([cropped_blob], "profile_picture.jpg");
                fd.append('profile_picture', profile_picture);
            }
            //profile_picture = $("#id_profile_picture").prop('files')[0];
            
            // Process member user form
            fd.append('csrfmiddlewaretoken', csrfmiddlewaretoken);
            fd.append('first_name', first_name);
            fd.append('last_name', last_name);
            fd.append('email', email);
            
            // Process member profile form
            fd.append('csrfmiddlewaretoken', csrfmiddlewaretoken);
            fd.append('affiliation', affiliation);
            fd.append('display_member', display_member);
            fd.append('recaptcha_token', recaptcha_token);

            
            // Post forms with ajax
            $.ajax({ // create an AJAX call...
                type: "POST", // GET or POST
                url: form_action_url,
                enctype: "multipart/form-data",
                data: fd,
                success: function(response) { // on success..
                    console.log("ajax success");
                },
                cache: false,
                contentType: false,
                processData: false,
                
            }).done(function (data) {
                
                if (data.success){
                    console.log("success");
                    $("#success-text").show();
                    $("#membership-form").remove();
                    //flash_message_with_ajax(data.success, "alert-success");

                }
                else if (data.error){
                    flash_message_with_ajax(data.error, "alert-danger");
                    $(".loading-dots-toggle").toggle();
                    $("#register-member-btn").removeClass("clicked");
                }
            }); // End of ajax

        }); // end of grecaptcha.execute
    }); // end of grecaptcha.ready

    return false;

}); // End of membershipform.submit

$("#id_profile_picture").change(function() {
    show_model_for_selected_file()
});




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