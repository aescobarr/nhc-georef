/* Undetermined nodes in jstree checkbox are those nodes selected because there is at least one
selected child node - it renders as a square in the checkbox */
var get_undetermined_nodes = function(tree_selector_string){
    var checked_ids = [];
    $(tree_selector_string)
        .find('.jstree-undetermined')
        .each(function (i, element) {
            var node_elem = '';
            var node_id = $(element).closest('.jstree-node').attr('id');
            var node_txt = $(element).closest('.jstree-node')[0].innerText.split('-')[0].trim();
            checked_ids.push(node_id+'$'+node_txt);
        });
    return checked_ids;
};

var get_top_selected_node = function(tree_selector_string){
    var top_selected_node_id = $(tree_selector_string).jstree().get_top_selected()[0];
    if (top_selected_node_id == null){
        return null;
    };
    var node_text = $('#' + top_selected_node_id)[0].innerText.split('-')[0].trim();
    return top_selected_node_id + '$' + node_text;
};

var get_full_selection_array = function(tree_selector_string){
    var checked = get_undetermined_nodes(tree_selector_string);
    var top_selected = get_top_selected_node(tree_selector_string);
    checked.push(top_selected);
    return checked;
};