var counter = 0;
var node_load_callback = function(node,status){
    counter=counter+1;
    if(counter < node_list.length ){
        if(!this.is_loaded(node_list[counter])){
            this.load_node(node_list[counter],node_load_callback);
        }
    }
    //This condition should only activate on second-to-last node
    if(counter == node_list.length - 1){
        //true/true avoids full selection when selecting deepest node
        this.select_node(node_list[counter],true,false);
        //From deepest node upwards, expand folders
        for(var i = node_list.length-2 ; i >= 0; i--){
            this.open_node(node_list[i]);
        }
    }
};

var init_ariadna = function(nodes){
    $('#ariadna ul').empty();
    for(var i = 0; i < nodes.length; i++){
        var id = nodes[i].split('$')[0];
        var nom = nodes[i].split('$')[1];
        var linkVisualitzar;
        if(i == 0){
            linkVisualitzar = '<li><a href="/toponims/update/' + id + '" title="'+nom+'">' + nom + '</a></li>';
        }else{
            linkVisualitzar = '<li><a href="/toponims/update/' + id + '" title="'+nom+'"> <- ' + nom + '</a></li>';
        }
        $('#ariadna ul').append(linkVisualitzar);
    }
};

var confirmDialog = function(message,id){
        $('<div></div>').appendTo('body')
            .html('<div><h6>'+message+'</h6></div>')
            .dialog({
                modal: true, title: 'Esborrant versió...', zIndex: 10000, autoOpen: true,
                width: 'auto', resizable: false,
                buttons: {
                    Yes: function () {
                        delete_versio(id);
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

var delete_versio = function(id){
    $.ajax({
        url: _versio_delete_url + id,
        method: "DELETE",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function( data, textStatus, jqXHR ) {
             toastr.success("Versió esborrada amb èxit!");
             $('table#versions tr#' + id).remove();
        },
        error: function(jqXHR, textStatus, errorThrown){
            toastr.error("Error esborrant la versió");
        }
    });
};

var refreshCentroidUI = function(){
    var centroid_data = djangoRef.Map.getCurrentCentroid();
    if(centroid_data != null){
        $('#id_coordenada_x_centroide').val( centroid_data.centroid.geometry.coordinates[0] );
        $('#id_coordenada_y_centroide').val( centroid_data.centroid.geometry.coordinates[1] );
        $('#id_precisio_h').val(centroid_data.radius * 1000);
    }else{
        $('#id_coordenada_x_centroide').val( '' );
        $('#id_coordenada_y_centroide').val( '' );
        $('#id_precisio_h').val( '' );
    }
};

$(document).ready(function() {

    $('#jstree')
        .on('loaded.jstree', function(event, data) {
            if(node_list != null && node_list.length>1 && node_list[0]!='1'){
                data.instance.load_node(node_list[0],node_load_callback);
            }else{
                data.instance.select_node(node_list[0]);
            }
        })
        .on('select_node.jstree', function (e, data) {
            $('#id_idpare').val(data.instance.get_top_selected()[0]);
        })
        .on('deselect_node.jstree', function (e, data) {
            if(data.instance.get_top_selected().length > 1){
                //top_selected_node = "";
                $('#id_idpare').val('');
            }else{
                //top_selected_node = data.instance.get_top_selected()[0];
                $('#id_idpare').val(data.instance.get_top_selected()[0]);
            }
        })
        .jstree({
            'plugins' : [
                'checkbox'
            ],
            'core' : {
                'multiple' : false,
                'data' : {
                    'url' : function (node) {
                        return node.id === '#' ? '/toponimstree/' : '/toponimstree/?id=' + node.id;
                    },
                    'data' : function (node) {
                        if(node.id=='#'){
                            return { 'id' : node_ini };
                        }else{
                            return { 'id' : node.id };
                        }
                    }
                }
            }
        });

    init_ariadna(node_list_full);

    /*$('#testbutton').click(function(){
        var checked = get_undetermined_nodes('#jstree');
        var top_selected = get_top_selected_node('#jstree');
        checked.push(top_selected);
    });*/

    var toponims =  {
        name: 'toponims',
        layer : L.tileLayer.wms(
            'http://127.0.0.1:8080/geoserver/mzoologia/wms?',
            {
                layers: 'mzoologia:toponimsdarreraversio',
                format: 'image/png',
                transparent: true
            }
        )
    };

    var overlay_list = [];
    overlay_list.push(toponims);

    var overlays_control_config = [
        {
            groupName: 'Toponims',
            expanded: true,
            layers: {
                'Darreres versions': toponims.layer
            }
        }
    ];

    map_options = {
        editable:true,
        show_centroid_after_edit: true,
        overlays: overlay_list,
        overlays_control_config: overlays_control_config,
        wms_url: wms_url
    };

    map_options.state = {
        overlays: [toponims.name],
        base: 'djangoRef.Map.roads',
        view:{ center:new L.LatLng(40.58, -3.25),zoom:2}
    };

    map = new djangoRef.Map.createMap(map_options);



    map.on(L.Draw.Event.CREATED, function (e) {
        refreshCentroidUI();
    });

    map.on(L.Draw.Event.EDITED, function (e) {
        refreshCentroidUI();
    });

    map.on(L.Draw.Event.DELETED, function (e) {
        refreshCentroidUI();
    });

});