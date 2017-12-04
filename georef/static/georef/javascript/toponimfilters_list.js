$(document).ready(function() {
    table = $('#toponimsfilter_list').DataTable( {
        "ajax": {
            "url": _filtrestoponims_list_url,
            "dataType": 'json'
        },
        "serverSide": true,
        "processing": true,
        //"language": opcions_llenguatge_catala,
        "pageLength": 25,
        "pagingType": "full_numbers",
        "bLengthChange": false,
        stateSave: true,
        "dom": '<"top"iflp<"clear">>rt<"bottom"iflp<"clear">>',
        stateSaveCallback: function(settings,data) {
            localStorage.setItem( 'DataTables_' + settings.sInstance, JSON.stringify(data) )
        },
        stateLoadCallback: function(settings) {
            return JSON.parse( localStorage.getItem( 'DataTables_' + settings.sInstance ) )
        },
        "columns": [
            { "data": "nomfiltre" }
            ,{ "data": "idfiltre" }
        ],
        "columnDefs": [
            {
                "targets":0,
                "title": "Nom del filtre"
            },
            {
                "targets":1,
                "title": "Id"
            }
        ]
    } );
});