var exportXLS = function(){
    var params = table.ajax.params();
    window.location.href = _toponims_list_xls + '?' + jQuery.param(params);
}

var exportKML = function(){
    var filtrejson = extreureJSONDeFiltre();
    if(filtrejson!=null && filtrejson!=''){
        var cql = transformarJSONACQL(filtrejson);
        var cql_filter_text = new OpenLayers.Format.CQL().write(cql);
        document.kml.CQL_FILTER.value = cql_filter_text;
    }else{
        document.kml.CQL_FILTER.value = "TRUE=TRUE";
    }
    document.kml.submit();
}

var exportSHP = function(){
    var filtrejson = extreureJSONDeFiltre();
    if(filtrejson!=null && filtrejson!=''){
        var cql = transformarJSONACQL(filtrejson);
        var cql_filter_text = new OpenLayers.Format.CQL().write(cql);
        document.shp.CQL_FILTER.value = cql_filter_text;
    }else{
        document.shp.CQL_FILTER.value = "TRUE=TRUE";
    }
    document.shp.submit();
}

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
            /*{
                'targets': 1,
                'data': 'editable',
                'sortable': false,
                'render': function(value){
                    if(value==true){
                        return '<button class="delete_button btn btn-danger"><i class="fa fa-times" aria-hidden="true"></i></button>';
                    }else{
                        return '&nbsp;';
                    }
                }
            },
            {
                'targets': 2,
                'data': 'editable',
                'sortable': false,
                'render': function(value){
                    if(value==true){
                        return '<button class="edit_button btn btn-info"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>';
                    }else{
                        return '&nbsp;';
                    }
                }
            },*/
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
            /*var activeOverlays = djangoRef.Map.getActiveOverlays();
            for(var i = 0; i < activeOverlays.length; i++){
                var layer = activeOverlays[i];
                filterCQL(ui.item.json,layer);
            }*/
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

});
