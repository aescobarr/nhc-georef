var getFeatureTypesInGeoJSON = function(geoJSON){
    var featureTypes = [];
    for(var i=0; geoJSON.features.length > i; i++){
        geom = geoJSON.features[i].geometry;
        featureTypes.push(geom.type);
    }
    return featureTypes;
}

var geoJSONIsSinglePoint = function(geoJSON){
    var featureTypes = getFeatureTypesInGeoJSON(geoJSON);
    if ($.inArray('Point',featureTypes) >= 0){
        if (geoJSON && geoJSON.features && geoJSON.features.length == 1){
            return true;
        }
    }
    return false;
}

function encodeQueryData(data) {
   const ret = [];
   for (let d in data)
     ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
   return ret.join('&');
}

var copyToClipboard = function (text) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val(text).select();
    document.execCommand("copy");
    $temp.remove();
}