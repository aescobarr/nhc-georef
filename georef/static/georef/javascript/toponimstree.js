$(function () {

    $('#jstree')
    .bind(
        "select_node.jstree", function(evt, data){
        if(selected_node != null){
            $("#" + selected_node.id + "_edit").remove();
        }
        if(data.node.id != '1'){
            var target_li = $('#' + data.node.id);
            target_li.append('<a id="' + data.node.id + '_edit" href="/toponims/update/' + data.node.id + '/-1"><i class="fa fa-pencil-square-o fa-2x" aria-hidden="true"></i></a>');
            selected_node = data.node;
        }
    })
    .jstree({
    'core' : {
        'data' : {
                "url" : function (node) {
                    return node.id === '#' ? '/toponimstree/' : '/toponimstree/?id=' + node.id;
                },
                'data' : function (node) {
                    return { 'id' : node.id };
                }
            }
        }
    });
});