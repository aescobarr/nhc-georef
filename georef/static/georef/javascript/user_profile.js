$(document).ready(function() {
    if(successfully_saved && successfully_saved==true){
        toastr.success('Dades actualitzades amb èxit!');
    }

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
            $('#id_idpare').val('');
        }else{
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
});