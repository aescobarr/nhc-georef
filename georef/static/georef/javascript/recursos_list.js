var exportXLS = function(){
    var params = table.ajax.params();
    window.location.href = _recursos_list_xls + '?' + jQuery.param(params);
}

var exportCSV = function(){
    var params = table.ajax.params();
    window.location.href = _recursos_list_csv + '?' + jQuery.param(params);
};

var exportPDF = function(){
    var params = table.ajax.params();
    window.location.href = _recursos_list_pdf + '?' + jQuery.param(params);
};

$(document).ready(function() {
    table = $('#recursos_list').DataTable( {
        'ajax': {
            'url': _recurs_list_url,
            'dataType': 'json',
            'data': function(d){
                var valorFiltre = getCookie('filtre_r');
                if(valorFiltre){
                    d.filtrejson = valorFiltre;
                }else{
                    d.filtrejson = extreureJSONDeFiltre();
                }
            }
        },
        'serverSide': true,
        'processing': true,
        //"language": opcions_llenguatge_catala,
        'pageLength': 25,
        'pagingType': 'full_numbers',
        'bLengthChange': false,
        stateSave: true,
        //"dom": '<"toolbar"><"top"iflp<"clear">>rt<"bottom"iflp<"clear">>',
        'dom': '<"top"iflp<"clear">>rt<"bottom"iflp<"clear">>',
        stateSaveCallback: function(settings,data) {
            localStorage.setItem( 'DataTables_' + settings.sInstance, JSON.stringify(data) );
        },
        stateLoadCallback: function(settings) {
            return JSON.parse( localStorage.getItem( 'DataTables_' + settings.sInstance ) );
        },
        'columns': [
            { 'data': 'nom' }
        ],
        'columnDefs': [
            {
                'targets': 1,
                'data': 'editable',
                'sortable': false,
                'defaultContent': '<button class="delete_button btn btn-danger"><i class="fa fa-times" aria-hidden="true"></i></button>'
                /*'render': function(value){
                    if(value==true){
                        return '<button class="delete_button btn btn-danger"><i class="fa fa-times" aria-hidden="true"></i></button>';
                    }else{
                        return '&nbsp;';
                    }
                }*/
            },
            {
                'targets': 2,
                'data': 'editable',
                'sortable': false,
                'defaultContent': '<button class="edit_button btn btn-info"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>'
                /*'render': function(value){
                    if(value==true){
                        return '<button class="edit_button btn btn-info"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>';
                    }else{
                        return '&nbsp;';
                    }
                }*/
            },
            {
                'targets':0,
                'title': 'Recurs de georeferenciació'
            }
        ]
    } );

    var check_nomfiltre = function(){
        var json = extreureJSONDeFiltre();
        var nomfiltre = $('#autoc_filtres').val();
        var modul = 'RECURSOS';
        $.ajax({
            url: _check_filtre_url,
            data: 'nomfiltre=' + encodeURI(nomfiltre) + "&modul=" + modul,
            method: 'GET',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                add_filtre(json,modul,nomfiltre);
            },
            error: function(jqXHR, textStatus, errorThrown){
                var idfiltre = jqXHR.responseJSON.detail;
                $( '#dialog-confirm' ).dialog({
                    resizable: false,
                    height: 'auto',
                    width: 400,
                    modal: true,
                    buttons: {
                        'Sobreescriure i filtrar': function() {
                            update_filtre(json,nomfiltre,idfiltre,modul);
                            $( this ).dialog( 'close' );
                        },
                        Cancel: function() {
                            $( this ).dialog( 'close' );
                        }
                    }
                });
            }
        });
    };

    $( '#addRecurs' ).click(function() {
        var url = '/recursos/create/';
        window.location.href = url;
    });

    var delete_recurs = function(id){
        $.ajax({
            url: _recurs_delete_url + id,
            method: 'DELETE',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                toastr.success('Recurs esborrat amb èxit!');
                table.ajax.reload();
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error('Error esborrant recurs');
            }
        });
    };

    var confirmDialog = function(message,id){
        $('<div></div>').appendTo('body')
            .html('<div><h6>'+message+'</h6></div>')
            .dialog({
                modal: true, title: 'Esborrant recurs...', zIndex: 10000, autoOpen: true,
                width: 'auto', resizable: false,
                buttons: {
                    Yes: function () {
                        delete_recurs(id);
                        $(this).dialog("close");
                    },
                    No: function () {
                        $(this).dialog("close");
                    }
                },
                close: function (event, ui) {
                    $(this).remove();
                }
        });
    };

    $('#autors_list tbody').on('click', 'td button.delete_button', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        var id = row.data().id;
        confirmDialog("Segur que vols esborrar?",id);
    });

    $('#recursos_list tbody').on('click', 'td button.edit_button', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        var id = row.data().id;
        url = '/recursos/update/' + id;
        window.location.href = url;
    });

    var add_filtre = function(json,modul,nomfiltre){
        var data = {
            'json': json,
            'modul': modul,
            'nomfiltre': nomfiltre
        };
        $.ajax({
            url: _filtres_create_url,
            method: 'POST',
            data: data,
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                toastr.success('Filtre desat amb èxit!');
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error('Error esborrant filtre!');
            }
        });
    };

    $( '#autoc_filtres' ).autocomplete({
        source: function(request,response){
            $.getJSON( _filtres_list_url + '?modul=RECURSOS&term=' + request.term, function(data){
                response($.map(data.results, function(item){
                    return {
                        label: item.nomfiltre,
                        value: item.idfiltre,
                        json: item.json
                    };
                }));
            });
        },
        minLength: 2,
        select: function( event, ui ) {
            var listname = ui.item.label;
            crearTaulaFiltre(ui.item.json);
            var activeOverlays = djangoRef.Map.getActiveOverlays();
            for(var i = 0; i < activeOverlays.length; i++){
                var layer = activeOverlays[i];
                filterCQL(ui.item.json,layer);
            }
            $('#autoc_filtres').val(listname);
            return false;
        }
    });

    $( '#saveDoFilter' ).click(function() {
        check_nomfiltre();
    });

    $( '#doFilter' ).click(function() {
        filter();
    });

    $( '#doClear' ).click(function() {
        clearTaula('taulafiltre');
        filter();
        $('#autoc_filtres').val('');
    });

    var importa_shapefile = function(filepath){
        $.ajax({
            url: _import_shapefile_url,
            data: 'path=' + encodeURI(filepath),
            method: 'GET',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                toastr.success('Importació amb èxit!');
                djangoRef.Map.editableLayers.clearLayers();
                var geoJson = JSON.parse(data.detail);
                var geoJSONLayer = L.geoJson(geoJson);
                geoJSONLayer.eachLayer(
                    function(l){
                        djangoRef.Map.editableLayers.addLayer(l);
                    }
                );
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error('Error important fitxer:' + jqXHR.responseJSON.detail);
            }
        });
    };

    var uploader = new qq.FileUploader({
        action: _ajax_upload_url,
        element: $('#fileuploader')[0],
        multiple: false,
        onComplete: function(id, fileName, responseJSON) {
            if(responseJSON.success) {
                //alert("success!");
                importa_shapefile(responseJSON.path);
            } else {
                alert('upload failed!');
            }
        },
        template:'<div class="qq-uploader">' +
            '<div class="qq-upload-drop-area"><span>Importar shapefile</span></div>' +
            '<div class="qq-upload-button ui-widget-content ui-button ui-corner-all ui-state-default">Importar shapefile</div>' +
            '<ul class="qq-upload-list"></ul>' +
            '</div>',
        params: {
            'csrf_token': csrf_token,
            'csrf_name': 'csrfmiddlewaretoken',
            'csrf_xname': 'X-CSRFToken',
        }
    });

    var recursos =  {
        name: 'recursos',
        layer : L.tileLayer.wms(
            'http://127.0.0.1:8080/geoserver/mzoologia/wms?',
            {
                layers: 'mzoologia:recursosgeoreferenciacio',
                format: 'image/png',
                transparent: true
            }
        )
    };

    var overlay_list = [];
    overlay_list.push(recursos);

    var overlays_control_config = [
        {
            groupName: 'Recursos de georeferenciació',
            expanded: true,
            layers: {
                'Recursos de georeferenciació (límits digitalitzats)': recursos.layer
            }
        }
    ];

    map_options = {
        editable:true,
        overlays: overlay_list,
        overlays_control_config: overlays_control_config,
        wms_url: wms_url
    };

    var valorView = getCookie('view_r');
    if(valorView){
        var jsonView = JSON.parse(valorView);
        map_options.center = jsonView.center;
        map_options.zoom = jsonView.zoom;
    }

    var valorEstat = getCookie('layers_r');
    if(valorEstat){
        var jsonState = JSON.parse(valorEstat);
        map_options.state = jsonState;
    }else{
        map_options.state = {
            overlays: [recursos.name],
            base: 'djangoRef.Map.roads',
            view:{ center:new L.LatLng(40.58, -3.25),zoom:2}
        };
    }

    map_options.consultable = [recursos.layer];

    map = new djangoRef.Map.createMap(map_options);
});
