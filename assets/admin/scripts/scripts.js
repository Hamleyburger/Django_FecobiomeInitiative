// Admin scripts

let hidden_columns = [];

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