$(document).ready(function() {
    $( '#autoc_toponim' ).autocomplete({
        source: function(request,response){
            $.getJSON( _toponim_search_url + '?term=' + request.term, function(data){
                response($.map(data.results, function(item){
                    return {
                        label: item.nom_str
                        ,value: item.nom_str
                        ,coord_x: item.coordenada_x_centroide
                        ,coord_y: item.coordenada_y_centroide
                        ,precisio: item.precisio
                        ,id: item.id
                        //,json: item.json
                    };
                }));
            });
        },
        minLength: 2,
        select: function( event, ui ) {
            var listname = ui.item.label;
            $('#autoc_toponim').val(listname);
            $('#val_nom').text(ui.item.label);
            $('#val_y').text(ui.item.coord_y);
            $('#val_x').text(ui.item.coord_x);
            $('#val_prec').text(ui.item.precisio);
            return false;
        }
    });

    $( '#clipboard' ).click(function() {
        var text = '';
        text = $('#val_nom').text() + ' lat:' + $('#val_y').text() + ' long:' + $('#val_x').text() + ' prec:' + $('#val_prec').text();
        copyToClipboard(text);
        toastr.success("Resultats copiats al portapapers!");
    });
});