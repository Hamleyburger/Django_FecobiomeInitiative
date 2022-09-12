$(document).ready(function() {
    $('#loading-div').css( "display", "none" );
    $('#hide-datatable').css( "display", "block" );
    $('#fi-datatable').DataTable( {
        responsive: true,
        colReorder: true,
        dom: 'Bfrtip', // to enable custom search builder add Q, to enable searchpanes add P (QPBfrtip)
        searchBuilder: true,
        SearchPanes: true,

        buttons: [
            { extend: 'csv', text: 'Get all results as CSV' },
            { extend: 'excel', text: 'Get all results as Excel' },
            { extend: 'colvis', text: 'Hide columns' },
        ],
        'oLanguage': {
            "sSearch": "Filter results"
        }

    });
} );

$("#version-links").change(function() {

    console.log(this.value);
    $("#dl-link").attr("href", this.value)
  });

