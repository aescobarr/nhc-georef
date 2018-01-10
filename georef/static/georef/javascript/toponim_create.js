var validate_toponim_create = function(){
    var top_selected = get_top_selected_node('#jstree');
    var checked = get_undetermined_nodes('#jstree');
    if (top_selected == null){
        toastr.error("Cal seleccionar un pare per al topònim")
        return false;
    }
    return true;
}

$(document).ready(function() {

    $('#jstree')
        /*.on('loaded.jstree', function(event, data) {
            if(node_list != null && node_list.length>1 && node_list[0]!='1'){
                data.instance.load_node(node_list[0],node_load_callback);
            }else{
                data.instance.select_node(node_list[0]);
            }
        })*/
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
});