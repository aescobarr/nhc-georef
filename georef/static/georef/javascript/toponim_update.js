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

var init_ariadna = function(){
    for(var i = 0; i < node_list_full.length; i++){
        var id = node_list_full[i].split('$')[0];
        var nom = node_list_full[i].split('$')[1];
        var linkVisualitzar;
        if(i == 0){
            //linkVisualitzar = '<li><a href="#" title="'+nom+'" onclick="javascript:visualitzar("'+id+'")">' + nom + '</a></li>';
            linkVisualitzar = '<li><a href="/toponims/update/' + id + '" title="'+nom+'">' + nom + '</a></li>';
        }else{
            //linkVisualitzar = '<li><a href="#" title="'+nom+'" onclick="javascript:visualitzar("'+id+'")"> <- ' + nom + '</a></li>';
            linkVisualitzar = '<li><a href="/toponims/update/' + id + '" title="'+nom+'"> <- ' + nom + '</a></li>';
        }
        $('#ariadna ul').append(linkVisualitzar);
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
                //top_selected_node = data.instance.get_top_selected()[0];
                $('#id_idpare').val(data.instance.get_top_selected()[0]);
            }
        )
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

    init_ariadna();
});