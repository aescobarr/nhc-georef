var counter = 0;
var tree;
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

var validate_toponim_create = function(){
    var top_selected = get_top_selected_node('#jstree');
    var checked = get_undetermined_nodes('#jstree');
    if (top_selected == null){
        toastr.error("Cal seleccionar un pare per al topònim")
        return false;
    }
    return true;
}

var create_tree = function(){
     return $('#jstree')
        .on('loaded.jstree', function(event, data) {
            if(node_list != null && node_list.length>1 && node_list[0]!='1'){
                data.instance.load_node(node_list[0],node_load_callback);
            }else{
                data.instance.select_node(node_list[0]);
            }
        })
        .on('select_node.jstree', function (e, data) {
            $('#id_idpare').val(data.instance.get_top_selected()[0]);
            $('#seleccio').empty();
            $('#seleccio').append('Seleccionat: ' + data.node.text);
        })
        .on('deselect_node.jstree', function (e, data) {
            if(data.instance.get_top_selected().length > 1){
                //top_selected_node = "";
                $('#id_idpare').val('');
                $('#seleccio').empty();
                $('#seleccio').append('Seleccionat: cap');
            }else{
                $('#id_idpare').val(data.instance.get_top_selected()[0]);
                $('#seleccio').empty();
                $('#seleccio').append('Seleccionat: ' + data.node.text);
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
                        if (node.id === '#'){
                            return '/toponimstree/';
                        }else{
                            return '/toponimstree/?id=' + node.id;
                        }
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
}

var reload_tree = function(node_list_full){
    node_list = [];
    for(var i = 0; i < node_list_full.length; i++){
        node_list.push(node_list_full[i].split('$')[0]);
    }
    var node_ini = "1";
    tree.jstree("destroy");
    counter = 0;
    tree = create_tree();
}

$(document).ready(function() {
    tree = create_tree();

    $( '#autoc_tree' ).autocomplete({
        source: function(request,response){
            $.getJSON( _toponim_node_search_url + '?term=' + request.term, function(data){
                response($.map(data, function(item){
                    return {
                        label: item.nom,
                        value: item.id,
                        node_list: item.node_list
                    };
                }));
            });
        },
        minLength: 3,
        select: function( event, ui ) {
            var listname = ui.item.label;
            $( '#autoc_tree' ).val(listname);
            reload_tree( ui.item.node_list );
            return false;
        }
    });
});