const db_choice = $("#id_database");
db_choice.change(function(event){

    console.log(event.target);
    console.log(event.target.value);
    console.log(fetch_resources_meta_url);
    $.ajax({
        // url is defined in submit_data.html
        url: fetch_resources_meta_url,
        data: {
          'key': event.target.value
        },
        method: "post",
        dataType: 'json',
        success: function (data) {
            $("#txt-dl-link").attr("href", data.txt_path);
            $("#xslx-dl-link").attr("href", data.xslx_path);
        }
      });

})