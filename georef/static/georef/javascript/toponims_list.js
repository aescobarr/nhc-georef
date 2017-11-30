$(document).ready(function() {
    table = $('#toponims_list').DataTable( {
        "ajax": {
            "url": _toponim_list_url,
            "dataType": 'json',
            "data": function(d){
                var valorFiltre = getCookie("filtre_t");
                if(valorFiltre){
                    d.filtrejson = valorFiltre;
                }else{
                    d.filtrejson = extreureJSONDeFiltre();
                }
            }
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
            { "data": "nom_str" }
            ,{ "data": "aquatic_str" }
            ,{ "data": "idtipustoponim.nom" }
        ],
        "columnDefs": [
            {
                "targets":0,
                "title": "Topònim"
            },
            {
                "targets":1,
                "title": "Aquàtic"
            },
            {
                "targets":2,
                "title": "Tipus"
            }
        ]
    } );

    $( "#autoc_filtres" ).autocomplete({
        source: function(request,response){
            $.getJSON( _filtres_list_url + "?term=" + request.term, function(data){
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
            //log( "Selected: " + ui.item.value + " aka " + ui.item.id );
            var listname = ui.item.label;
            var list_id = ui.item.value;
            toastr.info(ui.item);
            crearTaulaFiltre(ui.item.json);
            filterCQL(ui.item.json);
            $('#autoc_filtres').val(listname);
            return false;
        }
    });

    var add_filtre = function(json,modul,nomfiltre){
        var data = {
            "json": json,
            "modul": modul,
            "nomfiltre": nomfiltre
        };
        $.ajax({
            url: _filtres_create_url,
            method: "POST",
            data: data,
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                 toastr.success("Filtre desat amb èxit!");
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error("Error esborrant filtre!");
            }
        });
    }

    var update_filtre = function(json, nomfiltre, idfiltre, modul){
        var data = {
            "json": json,
            "modul": modul,
            "nomfiltre": nomfiltre
        };
        $.ajax({
            url: _filtres_update_url + idfiltre + "/",
            data: data,
            method: "PUT",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                 toastr.success("Filtre actualitzat amb èxit!");
                 filter();
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error("Error actualitzant filtre");
            }
        });
    }

    var delete_filtre = function(id){
        $.ajax({
            url: _filtres_delete_url + id,
            method: "DELETE",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                 toastr.success("Filtre esborrat amb èxit!");
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error("Error esborrant");
            }
        });
    };

    var check_nomfiltre = function(){
        var json = extreureJSONDeFiltre();
        var nomfiltre = $("#autoc_filtres").val();
        var modul = "TOPONIMS";
        $.ajax({
            url: _check_filtre_url,
            data: "nomfiltre=" + encodeURI(nomfiltre),
            method: "GET",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                 add_filtre(json,modul,nomfiltre);
            },
            error: function(jqXHR, textStatus, errorThrown){
                var idfiltre = jqXHR.responseJSON.detail;
                $( "#dialog-confirm" ).dialog({
                    resizable: false,
                    height: "auto",
                    width: 400,
                    modal: true,
                    buttons: {
                        "Sobreescriure i filtrar": function() {
                            update_filtre(json,nomfiltre,idfiltre,modul);
                            $( this ).dialog( "close" );
                        },
                        Cancel: function() {
                            $( this ).dialog( "close" );
                        }
                    }
                });
            }
        });
    };

    $( "#saveDoFilter" ).click(function() {
        check_nomfiltre();
    });

    $( "#doFilter" ).click(function() {
        filter();
    });

    $( "#doClear" ).click(function() {
        clearTaula('taulafiltre');
        filter();
        $('#autoc_filtres').val('');
    });

    var importa_shapefile = function(filepath){
        $.ajax({
            url: _import_shapefile_url,
            data: "path=" + encodeURI(filepath),
            method: "GET",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                 toastr.success("Importació amb èxit!");
                 editableLayers.clearLayers();
                 var geoJson = JSON.parse(data.detail);
                 var geoJSONLayer = L.geoJson(geoJson);
                 geoJSONLayer.eachLayer(
                    function(l){
                        editableLayers.addLayer(l);
                    }
                );
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error("Error important fitxer:" + textStatus);
            }
        });
    }

    var uploader = new qq.FileUploader({
        action: _ajax_upload_url,
        element: $('#fileuploader')[0],
        multiple: false,
        onComplete: function(id, fileName, responseJSON) {
            if(responseJSON.success) {
                //alert("success!");
                importa_shapefile(responseJSON.path);
            } else {
                alert("upload failed!");
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

});