$(document).ready(function() {
    $("#paraulaclau_list").tagit({
        singleField: true,
        autocomplete: {
            source: function( request, response ) {
                $.ajax({
                    url: "/api_internal/paraulesclau/",
                    dataType: "json",
                    data: {
                        featureClass: "P",
                        style: "full",
                        maxRows: 12,
                        name: request.term
                    },
                    success: function( data ) {
                         response( $.map( data.results, function( item ) {
                            return {
                                label: item.paraula,
                                value: item.paraula
                            }
                         }));
                    }
                });
            },
            minLength: 2,
            preprocessTag: function (val) {
                if (!val) {
                    return '';
                }
                return val.toLowerCase();
            }
        },
        fieldName: "paraulesclau"
    });

    $("#autor_list").tagit({
        singleField: true,
        autocomplete: {
            source: function( request, response ) {
                $.ajax({
                    url: "/api_internal/autors/",
                    dataType: "json",
                    data: {
                        featureClass: "P",
                        style: "full",
                        maxRows: 12,
                        name: request.term
                    },
                    success: function( data ) {
                         response( $.map( data.results, function( item ) {
                            return {
                                label: item.nom,
                                value: item.nom
                            }
                         }));
                    }
                });
            },
            minLength: 2,
            preprocessTag: function (val) {
                if (!val) {
                    return '';
                }
                return val.toLowerCase();
            }
        },
        fieldName: "autors",
        allowSpaces: true
    });

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