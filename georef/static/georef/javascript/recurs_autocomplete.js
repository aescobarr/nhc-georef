$(document).ready(function() {
    $("#paraulaclau_list").tagit({
        singleField: true,
        singleFieldDelimiter: '#',
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
        fieldName: "paraulesclau",
        allowSpaces: true
    });

    $("#autor_list").tagit({
        singleField: true,
        singleFieldDelimiter: '#',
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
});