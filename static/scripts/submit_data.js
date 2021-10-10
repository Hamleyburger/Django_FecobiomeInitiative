const db_choice = $("#id_database");
db_choice.change(function(event){

    $.ajax({
        // url is defined in submit_data.html
        url: fetch_resources_meta_url,
        data: {
          'key': event.target.value
        },
        method: "post",
        dataType: 'json',
        success: function (data) {
            // static_root is defined in head of base.html
            $("#txt-dl-link").attr("href", static_root + data.txt_path);
            $("#xlsx-dl-link").attr("href", static_root + data.xlsx_path);
        }
      });

})