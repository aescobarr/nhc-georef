function anarAUrl(inputId){
    window.open ( $('#'+inputId).val() ,'_blank');
    window.focus();
}

function showListToponims(){
    $( "#dialogListToponims" ).dialog( "open" );
}

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

    var init_toponims_basats_recurs = function(nodes){
        $('#toponimsbasats ul').empty();
        for(var i = 0; i < toponims_basats_recurs.length; i++){
            var id = toponims_basats_recurs[i].id;
            var nom = toponims_basats_recurs[i].nom;
            var linkVisualitzar = '<li><a target="_blank" href="/toponims/update/' + id + '/-1" title="'+nom+'"><span class="label label-default">' + nom + '</span></a></li>';
            $('#toponimsbasats ul').append(linkVisualitzar);
        }
        if(moretoponims){
            $('#toponimsbasats ul').append('<li><a onclick="javascript:showListToponims();" href="#">...</a></li>');
        }
    };

    init_toponims_basats_recurs();

    var target = $('#toponimsbasats');

    $( "#dialogListToponims" ).dialog({
        autoOpen: false,
        show: "blind",
        hide: "explode",
        height: 400,
        width: 350
    });

});