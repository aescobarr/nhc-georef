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

/* Undetermined nodes in jstree checkbox are those nodes selected because there is at least one
selected child node - it renders as a square in the checkbox */
var get_undetermined_nodes = function(){
    var checked_ids = [];
    $('#jstree')
        .find('.jstree-undetermined')
        .each(function (i, element) {
            var node_elem = '';
            var node_id = $(element).closest('.jstree-node').attr('id');
            var node_txt = $(element).closest('.jstree-node')[0].innerText.split('-')[0].trim();
            checked_ids.push(node_id+'$'+node_txt);
        });
    return checked_ids;
};

var get_top_selected_node = function(){
    var top_selected_node_id = $('#jstree').jstree().get_top_selected()[0];
    var node_text = $('#' + top_selected_node_id)[0].innerText.split('-')[0].trim();
    return top_selected_node_id + '$' + node_text;
};

var get_full_selection_array = function(){
    var checked = get_undetermined_nodes();
    var top_selected = get_top_selected_node();
    checked.push(top_selected);
    return checked;
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
    $('#testbutton').click(function(){
        var checked = get_undetermined_nodes();
        var top_selected = get_top_selected_node();
        checked.push(top_selected);
    });
});