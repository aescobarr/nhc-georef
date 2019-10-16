$(document).ready(function() {

    table = $('#prefscapes').DataTable( {
        "ajax": {
            "url": _capawmslocal_list_url,
            "dataType": 'json'
            ,"data": function(d){
                d.filtrejson = '{"filtre":[{"idrecurs":"*"}]}';
            }
        },
        "serverSide": true,
        "processing": true,
        "language": opcions_llenguatge,
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
            { "data": "name" }
            ,{ "data": "label" }
            ,{ "data": "baseurlservidor" }
            ,{ "data": "visible" }
        ],
        "columnDefs": [
            {
                "targets":0,
                "title": gettext("Nom de la capa")
            },
            {
                "targets":1,
                "title": gettext("Títol de la capa")
            },
            {
                "targets":2,
                "title": gettext("URL servidor wms")
            },
            {
                "targets": 3,
                "title": gettext("Mostrar capa"),
                "render": function(value){
                    var retVal = "";
                    if(value){
                        retVal += '<input type="checkbox" class="visible_chk" checked/>';
                    }else{
                        retVal += '<input type="checkbox" class="visible_chk"/>';
                    }
                    return retVal;
                },
                "sortable": false
            }
        ]
    } );

    var toggle_prefs = function(layer_id, pref_value){
        $.ajax({
            url: _toggle_prefs_wms,
            data: 'id=' + encodeURI(layer_id) + '&value=' + encodeURI(pref_value),
            method: 'POST',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                table.ajax.reload(null,false);
            },
            error: function(jqXHR, textStatus, errorThrown){
                table.ajax.reload(null,false);
            }
        });
    }

    $('#prefscapes tbody').on('click', 'td input.visible_chk', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        var id = row.data().id
        console.log($(this).is(":checked"));
        toggle_prefs(id, $(this).is(":checked"));
    });

});