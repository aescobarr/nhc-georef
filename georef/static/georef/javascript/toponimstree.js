$(function () {

    $('#jstree')
    .bind(
        "select_node.jstree", function(evt, data){
        if(selected_node != null){
            $("#" + selected_node.id + "_edit").remove();
        }
        var target_li = $('#' + data.node.id);
        target_li.append('<a id="' + data.node.id + '_edit" href="/toponims/update/' + data.node.id + '"><i class="fa fa-pencil-square-o fa-2x" aria-hidden="true"></i></a>');
        selected_node = data.node;
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
        /*'data': [
                    {"text": "M\u00f3n", "id": "1", "parent": "#"},
                    {"text": "\u00c0frica - None (continent) (N)", "id": "mlozano3506592866400701903", "parent": "1"},
                    {"text": "\u00c0sia - None (continent) (N)", "id": "furibe7849454840029027962", "parent": "1"},
                    {"text": "Am\u00e8rica - None (continent) (N)", "id": "furibe80145712157109061375", "parent": "1"},
                    {"text": "Oceania - None (continent) (N)", "id": "furibe80146450619579101381", "parent": "1"},
                    {"text": "Europa - None (continent) (N)", "id": "furibe80116566346802081369", "parent": "1"},
                    {"text": "Mars i oceans - None (accident geogr\u00e0fic) (S)", "id": "furibe33628913638886373", "parent": "1"}
                ]
        }*/
    });
});