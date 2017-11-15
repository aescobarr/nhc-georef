$(document).ready(function() {
    var table = $('#toponims_list').DataTable( {
        "ajax": {
            "url": "/georef/datatabletoponims/list",
            "dataType": 'json'
        },
        "serverSide": true,
        "processing": true,
        //"language": opcions_llenguatge_catala,
        "pageLength": 25,
        "pagingType": "full_numbers",
        "bLengthChange": false,
        stateSave: true,
        stateSaveCallback: function(settings,data) {
            localStorage.setItem( 'DataTables_' + settings.sInstance, JSON.stringify(data) )
        },
        stateLoadCallback: function(settings) {
            return JSON.parse( localStorage.getItem( 'DataTables_' + settings.sInstance ) )
        },
        "columns": [
            { "data": "nom" }
            ,{ "data": "aquatic" }
        ],
        "columnDefs": [
            {
                "targets":0,
                "title": "Topònim"
            },
            {
                "targets":1,
                "title": "Aquàtic"
            }
        ]
    } );
});