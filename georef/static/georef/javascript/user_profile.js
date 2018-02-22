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
        this.select_node(node_list[counter],true,true);
        //From deepest node upwards, expand folders
        for(var i = node_list.length-2 ; i >= 0; i--){
            this.open_node(node_list[i]);
        }
    }
};

var checkPermissions = function(){
    $('.form-errors').empty();
    if( $('#id_permission_toponim_edition').is(":checked") ){
        if($('#id_toponim_permission').val()==''){
            $('.form-errors').append('<p class="error">Cal seleccionar a l\'arbre de topònims el topònim superior que es té permís per editar. Per tenir permís per editar qualsevol topònim, seleccionar \'Tots els topònims\'</p>');
            return false;
        }
    }else{
        if($('#id_toponim_permission').val()!=''){
            $('#jstree').jstree("deselect_all");
            $('#id_toponim_permission').val("");
            return true;
        }
    }
    return true;
};

$(document).ready(function() {
    if(successfully_saved && successfully_saved==true){
        toastr.success('Dades actualitzades amb èxit!');
    }

    if(successfully_saved && successfully_saved==false){
        toastr.success('Error desant dades!');
    }

    $('#jstree')
    .on('loaded.jstree', function(event, data) {
        if(node_list != null && node_list.length>1){
            data.instance.load_node(node_list[0],node_load_callback);
        }
        else{
            data.instance.select_node(node_list[0]);
        }
    })
    .on('select_node.jstree', function (e, data) {
        $('#id_toponim_permission').val(data.instance.get_top_selected()[0]);
    })
    .on('deselect_node.jstree', function (e, data) {
        if(data.instance.get_top_selected().length > 1){
            $('#id_toponim_permission').val('');
        }else{
            $('#id_toponim_permission').val(data.instance.get_top_selected()[0]);
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
                    /*if(node.id=='#'){
                        return { 'id' : node_ini };
                    }else{
                        return { 'id' : node.id };
                    }*/
                    return { "id" : node.id };
                }
            }
        }
    });

    $('#id_permission_toponim_edition').change(function() {
        if(!$(this).is(":checked")) {
            $('#jstree').jstree("deselect_all");
        }
    });
});