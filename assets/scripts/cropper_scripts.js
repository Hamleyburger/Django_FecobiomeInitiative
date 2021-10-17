
// Using #croppermodal, #id_profile_picture, #cropperimage #cropper-confirm #preview from "html for cropper scripts"
// Insert this script before the script that is going to use the resulting file. The fil is accessible as cropped_blob
// File input element that triggers cropper modal must have id #id_profile_picture (or be refactored)
// check if cropped_blob is null, if not it can be appended to formData or downloaded or whatever.


// Let cropper be accessible from various functions and event listeners
let global_cropper;

// There is this image element in the cropper modal.
let image_element = $('#id_profile_picture')[0];

// cropper_formData will contain a "file" entry if a file has been modified in the cropper.
let cropped_blob = null;






// When file is selected from a form show a cropper modal for editing it
function show_model_for_selected_file() {
    // Show cropper modal if there is a valid file

    var files = image_element.files;

    if(files.length > 0 ){
        file = files[0];
        if (prevalidate_image_type(file)) {
            show_cropper_modal();
        }
    }
}


function upload_file(url_for_img_upload, image_file_form) {

    // Attempt to upload file to server
    $.ajax({

        type: 'POST',
        url: url_for_img_upload,
        data: image_file_form,
        contentType: false,
        cache: false,
        processData: false,

    }).done(function(data) {

        if (data.error) {
            alert("Server returned an error.");

        }
    }); 
}




// prevalidate image returns true if type (extension) is jpg or png
function getType(file) {
    var t = file.type.split('/').pop().toLowerCase();
    if (t.toUpperCase() === "JPEG".toUpperCase() || t.toUpperCase() === "JPG".toUpperCase()) {
        return "jpeg";
    }
    else if (t.toUpperCase() === "PNG".toUpperCase()) {
        return "png";
    }
    else {
        return t
    }
}

function prevalidate_image_type(file) {

    // This is here to save the user from wasting time on cropping images that won't get accepted by the server anyway
    var t = getType(file);

    if (t != "jpeg" && t != "jpg" && t != "png") {
        alert('File must be .png or .jpg');
        document.getElementById("id_profile_picture").value = '';
        return false;
    }

    return true;
}




// Cropper can only be started when modal is shown. Destroy cropper when modal is gone.
// Shows croppermodal with id croppermodal
function show_cropper_modal() {
    // when this modal is ready and shown cropper is started
    $("#croppermodal").modal("show");
}

// on show modal start cropper (ot cropper won't load right)
$('#croppermodal').on('shown.bs.modal', function () {
    // Cropper is always in modal and modal does not exist without cropper
    start_cropper();
})

// on hide modal destroy cropper
$('#croppermodal').on('hidden.bs.modal', function () {

    $("#id_profile_picture").html("");
    $("#id_profile_picture").val("");
    const image = document.getElementById('cropperimage');
    image.cropper.destroy();

});



// Resizes an image (max_width_or_height is pixels) and returns a URL
function get_resized_url(file, max_width_or_height) {

    return new Promise(resolve => {

        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function (event) {
            const imgElement = document.createElement("img");
            // Event.target.result is the URL to be put in a src
            imgElement.src = event.target.result;
            // Document.querySelector("#input").src = event.target.result;
            
            imgElement.onload = function (e) {

                const canvas = document.createElement("canvas");
                const MAX_WIDTH_OR_HEIGHT = max_width_or_height;
                
                let canvas_width = this.width;
                let canvas_height = this.height;

                // First find the biggest side, then scale it down
                if (this.width > this.height) {
                    // Scale down with width as the biggest size
                    if (this.width > MAX_WIDTH_OR_HEIGHT) {
                        const scaleSize = MAX_WIDTH_OR_HEIGHT / e.target.width;
                        canvas_width = MAX_WIDTH_OR_HEIGHT;
                        canvas_height = e.target.height * scaleSize;
                    }
                }
                else {
                    // Scale down with height as the biggest size
                    if (this.height > MAX_WIDTH_OR_HEIGHT) {
                        const scaleSize = MAX_WIDTH_OR_HEIGHT / e.target.height;
                        canvas_height = MAX_WIDTH_OR_HEIGHT;
                        canvas_width = e.target.width * scaleSize;
                    }

                }

                // canvas height and width will need to be adjusted to the image in any case
                canvas.width = canvas_width;
                canvas.height = canvas_height;
                const ctx = canvas.getContext("2d");
                ctx.drawImage(e.target, 0, 0, canvas.width, canvas.height);
                const srcEncoded = ctx.canvas.toDataURL(e.target, "image/jpeg");
                
                resolve(srcEncoded);
            };
        };
    });
}


// initialize cropper. Take image with id image (input image from form), resize and put in cropper.
async function start_cropper() {

    const image = document.getElementById('cropperimage'); // Define cropper element
    const input = $("#id_profile_picture"); // Get input field
    const input_image_file = input[0].files[0]; // Get image from input field
    const image_url = await get_resized_url(input_image_file, 800); // Make URL for image
    // const image_url = // Get url from variable.
    
    const cropper = new Cropper(image, {

        aspectRatio: 1 / 1,
        viewMode: 2,
        preview: $("#preview"),
        autoCropArea: 1,
        movable: false,
        rotatable: false,
        responsive: true,

    });

    // Make sure image is replaced every time start_cropper is called
    image.cropper.replace(image_url);
    global_cropper = image.cropper;

}


// Confirm buttons saves image and closes cropper
$("#cropper-confirm").click(function() {

    var file = image_element.files[0];
    var filetype = getType(file);
    var mimetype = "image/" + filetype
    var filename = "x." + filetype // Server does not like extensionless files


    global_cropper.getCroppedCanvas().toBlob((blob) => { // GetCroppedCanvas is a cropperjs function
        cropped_blob = blob;
        console.log(blob);
    },
    mimetype
    );

    // Hiding modal triggers destruction of cropper
    $("#croppermodal").modal("hide");

});

