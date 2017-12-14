$(document).ready(function() {
    $('#jstree')
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