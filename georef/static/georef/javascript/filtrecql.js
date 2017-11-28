function transformarJSONACQL(jsonStringFiltre){
    var filtre = null;
    var jsonFiltre = JSON.stringify(jsonStringFiltre);
    var condicions = jsonFiltre.filtre;
    for (var i=0; i<condicions.length; i++){
        filtre = transformarCondicioFiltreJSONACQL(filtre,condicions[i].operador,condicions[i].condicio,condicions[i].valor,condicions[i].not);

    }
    return filtre;
}


function transformarCondicioFiltreJSONACQL(filtreAnterior,operador,condicio,valor,not){
    var filtre,filtreNou;

    if('nom'==condicio){
        if('S'==not){
            filtreNou = transformarNotCQL(transformarCondicioPartNomACQL(valor));
        }else{
            filtreNou = transformarCondicioPartNomACQL(valor);
        }
    }else if('tipus'==condicio){
        if('S'==not){
            filtreNou = transformarNotCQL(transformarCondicioTipusACQL(valor));
        }else{
            filtreNou = transformarCondicioTipusACQL(valor);
        }
    }else if('pais'==condicio){
        if('S'==not){
            filtreNou = transformarNotCQL(transformarCondicioPaisACQL(valor));
        }else{
            filtreNou = transformarCondicioPaisACQL(valor);
        }
    }else if('aquatic'==condicio){
        if('S'==not){
            filtreNou = transformarNotCQL(transformarCondicioAquaticACQL(valor));
        }else{
            filtreNou = transformarCondicioAquaticACQL(valor);
        }
    }else if('geografic'==condicio){
        var elem;
        var filtreGeoNou,filtreGeoTotal;
        for(i=0;i<vectors.features.length;i++){
            elem = vectors.features[i].geometry;
            elemFiltre = elem.clone();
            elemFiltre.transform(new OpenLayers.Projection("EPSG:900913"), new OpenLayers.Projection("EPSG:4326"));
            if('S'==not){
                filtreGeoNou = transformarNotCQL(transformarCondicioGeograficACQL(elemFiltre));
            }else{
                filtreGeoNou = transformarCondicioGeograficACQL(elemFiltre);
            }
            if(filtreGeoTotal!=null){
                filtreGeoTotal = new OpenLayers.Filter.Logical({
                    type: OpenLayers.Filter.Logical.OR,
                    filters: [filtreGeoTotal,filtreGeoNou]
                });
            }else{
                filtreGeoTotal = filtreGeoNou;
            }
        }
        filtreNou = filtreGeoTotal;
    }

    if(filtreAnterior!=null && 'and'==operador){
        filtre = new OpenLayers.Filter.Logical({
        type: OpenLayers.Filter.Logical.AND,
        filters: [filtreAnterior,filtreNou]
            });
    }else if(filtreAnterior!=null && 'or'==operador){
        filtre = new OpenLayers.Filter.Logical({
        type: OpenLayers.Filter.Logical.OR,
        filters: [filtreAnterior,filtreNou]
            });
    }else{
        filtre = filtreNou;
    }
    return filtre;
}