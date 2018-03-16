$(document).ready(function() {
    var buildTagsUI = function (){
        var paraula_array = paraulesclau.split(",");
        $("#paraulaclau_list").tagit("removeAll");
        for(var i = 0; i < paraula_array.length; i++){
            $("#paraulaclau_list").tagit("createTag", paraula_array[i]);
        }
        var autor_array = autors.split(",");
        $("#autor_list").tagit("removeAll");
        for(var i = 0; i < autor_array.length; i++){
            $("#autor_list").tagit("createTag", autor_array[i]);
        }
    };

    buildTagsUI();
});