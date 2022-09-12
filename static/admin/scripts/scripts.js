// Admin scripts

let hidden_columns = [];

// Collapsing columns (until next search) in admin list view for Data
$(".collapse-column-btn").click(function(event) {
    event.preventDefault();
    index = $(this).data("column");
    headers = $(".results thead ").find("th");
    fields = $(".results tbody").find("tr");
    header = headers.get(index)

    $(this).toggleClass("selected");
    $(header).toggleClass("hidden-column");
    fields.each(function(i) {
        field = $(this).children().get(index);
        $(field).toggleClass("hidden-column");
    });
});



$("#preview-button").click(function() {
    console.log("clicked preview");
    $("#preview-section").toggle();
    $("#input-section").toggle();
    var subject_text = $("#id_subject").val();
    var message_rich_text = CKEDITOR.instances['id_message'].getData();
    $("#preview-subject").html(subject_text);
    $("#preview-message").html(message_rich_text);

});
$("#edit-button").click(function() {
    console.log("clicked edit");
    $("#preview-section").toggle();
    $("#input-section").toggle();
});