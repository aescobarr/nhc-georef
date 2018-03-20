var refreshDigitizedGeometry = function(){
    var geometry = djangoRef.Map.editableLayers.toGeoJSON();
    var json_string = JSON.stringify(geometry);
    $('#geometria').val( json_string );
};

function anarAUrl(inputId){
    window.open ( $('#'+inputId).val() ,'_blank');
    window.focus();
}

function showListToponims(){
    $( "#dialogListToponims" ).dialog( "open" );
}

$(document).ready(function() {
    var buildTagsUI = function (){
        var paraula_array = paraulesclau.split(",");
        $("#paraulaclau_list").tagit("removeAll");
        for(var i = 0; i < paraula_array.length; i++){
            $("#paraulaclau_list").tagit("createTag", paraula_array[i]);
        }
        var autor_array = autors.split(",");
        $("#autor_list").tagit("removeAll");
        for(var i = 0; i < autor_array.length; i++){
            $("#autor_list").tagit("createTag", autor_array[i]);
        }
    };

    buildTagsUI();

    var init_toponims_basats_recurs = function(nodes){
        $('#toponimsbasats ul').empty();
        for(var i = 0; i < toponims_basats_recurs.length; i++){
            var id = toponims_basats_recurs[i].id;
            var nom = toponims_basats_recurs[i].nom;
            var linkVisualitzar = '<li><a target="_blank" href="/toponims/update/' + id + '/-1" title="'+nom+'"><span class="label label-default">' + nom + '</span></a></li>';
            $('#toponimsbasats ul').append(linkVisualitzar);
        }
        if(moretoponims){
            $('#toponimsbasats ul').append('<li><a onclick="javascript:showListToponims();" href="#">...</a></li>');
        }
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
                djangoRef_map.editableLayers.clearLayers();
                var geoJson = JSON.parse(data.detail);
                var geoJSONLayer = L.geoJson(geoJson);
                geoJSONLayer.eachLayer(
                    function(l){
                        djangoRef_map.editableLayers.addLayer(l);
                    }
                );
                refreshDigitizedGeometry();
                djangoRef_map.editableLayers.bringToFront();
                if(djangoRef_map.editableLayers.getBounds().isValid()){
                    djangoRef_map.map.fitBounds(djangoRef_map.editableLayers.getBounds());
                }
                toastr.success('Importació amb èxit!');
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error('Error important fitxer:' + jqXHR.responseJSON.detail);
            }
        });
    };

    init_toponims_basats_recurs();

    var target = $('#toponimsbasats');

    $( "#dialogListToponims" ).dialog({
        autoOpen: false,
        show: "blind",
        hide: "explode",
        height: 400,
        width: 350
    });

    var toponims_b_recurs =  {
        name: 'toponims_b_recurs',
        layer : L.tileLayer.wms(
            'http://127.0.0.1:8080/geoserver/mzoologia/wms?',
            {
                layers: 'mzoologia:toponimsbasatsenrecurs',
                format: 'image/png',
                transparent: true,
                CQL_FILTER: cql_filter_ini
            }
        )
    };

    var overlay_list = [];
    overlay_list.push(toponims_b_recurs);

    var overlays_control_config = [
        {
            groupName: 'Toponims',
            expanded: true,
            layers: {
                'Topònims basats en recurs': toponims_b_recurs.layer
            }
        }
    ];

    map_options = {
        editable:true,
        show_centroid_after_edit: false,
        show_coordinates: false,
        overlays: overlay_list,
        overlays_control_config: overlays_control_config,
        wms_url: wms_url
    };

    map_options.state = {
        overlays: [toponims_b_recurs.name],
        base: 'djangoRef.Map.roads',
        view:{ center:new L.LatLng(40.58, -3.25),zoom:2}
    };

    djangoRef_map = new djangoRef.Map.createMap(map_options);

    djangoRef_map.map.on(L.Draw.Event.CREATED, function (e) {
        refreshDigitizedGeometry();
    });

    djangoRef_map.map.on(L.Draw.Event.EDITED, function (e) {
        refreshDigitizedGeometry();
    });

    djangoRef_map.map.on(L.Draw.Event.DELETED, function (e) {
        refreshDigitizedGeometry();
    });

    var geoJSONLayer = L.geoJson(geometries_json);
    geoJSONLayer.eachLayer(
        function(l){
            djangoRef_map.editableLayers.addLayer(l);
        }
    );

    refreshDigitizedGeometry();
    djangoRef_map.editableLayers.bringToFront();
    if(djangoRef_map.editableLayers.getBounds().isValid()){
        djangoRef_map.map.fitBounds(djangoRef_map.editableLayers.getBounds());
    }

});