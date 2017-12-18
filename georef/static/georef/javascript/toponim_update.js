var counter = 0;
var node_load_callback = function(node,status){
    counter=counter+1;
    //this.open_node(node);
    if(counter < node_list.length ){
        if(!this.is_loaded(node_list[counter])){
            this.load_node(node_list[counter],node_load_callback);
        }
    }
    //Aquesta condició es dona al carregar el darrer node
    if(counter == node_list.length - 1){
        //El true/true és per evitar que al seleccionar el node més profund,
        //es seleccioni tota la taula
        this.select_node(node_list[counter],true,true);
        //Des del node més profund amunt, anem desplegant carpetes
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
            linkVisualitzar = '<li><a href="#" title="'+nom+'" onclick="javascript:visualitzar("'+id+'")">' + nom + '</a></li>';
        }else{
            linkVisualitzar = '<li><a href="#" title="'+nom+'" onclick="javascript:visualitzar("'+id+'")">' + nom + '</a></li>';
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
        }).jstree({
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