$(document).ready(function() {
    $('#loading-div').css( "display", "none" );
    $('#hide-datatable').css( "display", "block" );
    $('#fi-datatable').DataTable( {
        responsive: true,
        colReorder: true,
        dom: 'Bfrtip',
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

