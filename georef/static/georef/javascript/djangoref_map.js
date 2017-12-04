(function(){

if (typeof(L) == 'undefined' || typeof(L.map) == 'undefined') throw "Leaflet map library must be loaded";

if (typeof(L.gridLayer.googleMutant) == 'undefined') throw "Google Mutant leaflet library must be loaded";

if (typeof djangoRef === 'undefined') this.djangoRef = {};

if (typeof djangoRef.Map === 'undefined') this.djangoRef.Map = {};

var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';

djangoRef.Map.osm = new L.TileLayer(
    osmUrl,
    {minZoom: 2, maxZoom: 12, attribution: osmAttrib}
);

djangoRef.Map.roads = L.gridLayer.googleMutant({
    type: 'roadmap' // valid values are 'roadmap', 'satellite', 'terrain' and 'hybrid'
});

djangoRef.Map.satellite = L.gridLayer.googleMutant({
    type: 'satellite' // valid values are 'roadmap', 'satellite', 'terrain' and 'hybrid'
});

djangoRef.Map.terrain = L.gridLayer.googleMutant({
    type: 'terrain' // valid values are 'roadmap', 'satellite', 'terrain' and 'hybrid'
});

djangoRef.Map.hybrid = L.gridLayer.googleMutant({
    type: 'hybrid' // valid values are 'roadmap', 'satellite', 'terrain' and 'hybrid'
});

djangoRef.Map.overlays = {};

djangoRef.Map.map = null;

/*
djangoRef.Map.toponims =  L.tileLayer.wms(
    'http://127.0.0.1:8080/geoserver/mzoologia/wms?',
    {
        layers: 'mzoologia:toponimsdarreraversio',
        format: 'image/png', transparent: true
    }
);
*/

djangoRef.Map.editableLayers = new L.FeatureGroup();
//var editableLayers = new L.FeatureGroup();

djangoRef.Map.createMap = function(options) {
    options = options || {};
    options = $.extend({},
    {
        div: 'map',
        center: new L.LatLng(40.58, -3.25),
        zoom: 2,
        consultable: [],
        editable: false,
        overlays: []
    },options);

    var map;

    map = new L.Map(options.div);

    var baseMaps = [
        {
            groupName: "Open Street Maps",
            expanded: true,
            layers: {
                "Open Street Map": djangoRef.Map.osm
            }
        },
        {
            groupName: "Google Base Maps",
            expanded: true,
            layers: {
                "Google roads": djangoRef.Map.roads,
                "Google satellite": djangoRef.Map.satellite,
                "Google terrain": djangoRef.Map.terrain,
                "Google hybrid": djangoRef.Map.hybrid
            }
        }
    ];

    var overlays_control_config = options.overlays_control_config;

    var controlCapes_options = {
		container_width 	: "180px",
		container_height    : "500px",
		container_maxHeight : "500px",
		group_maxHeight     : "120px",
		exclusive       	: false
	};

	if(options.editable){

        var draw_options = {
            position: 'topleft',
            draw: {
                polyline: {
                    shapeOptions: {
                        color: '#f357a1',
                        weight: 10
                    }
                },
                polygon: {
                    allowIntersection: false, // Restricts shapes to simple polygons
                    drawError: {
                        color: '#e1e100', // Color the shape will turn when intersects
                        message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
                    },
                    shapeOptions: {
                        color: '#bada55'
                    }
                },
                circle: false, // Turns off this drawing tool
                rectangle: {
                    shapeOptions: {
                        clickable: false
                    }
                },
                /*marker: {
                    icon: new MyCustomMarker()
                }*/
                marker: false,
                circlemarker: false
            },
            edit: {
                featureGroup: djangoRef.Map.editableLayers, //REQUIRED!!
                remove: true
            }
        };

        var drawControl = new L.Control.Draw(draw_options);
        map.addControl(drawControl);
        map.addLayer(djangoRef.Map.editableLayers);

    }

    controlCapes = L.Control.styledLayerControl(baseMaps, overlays_control_config, controlCapes_options);
	map.addControl(controlCapes);
	controlCapes.selectLayer(djangoRef.Map.osm);

	map.setView(options.center,options.zoom);

	if(options.consultable && options.consultable.length > 0){
        map.on('click', function(evt){
            var param_layers = [];
            for(var i=0; i < options.consultable.length; i++){
                param_layers.push( options.consultable[i].wmsParams.layers );
            };
            var querylayers = param_layers.join(',');
            getFeatureInfo(evt,querylayers);
        });
    }

    if(options.overlays && options.overlays.length > 0){
        register_overlays(options.overlays);
    }

    if(options.state){
        djangoRef.Map.setState(options.state);
    }

    djangoRef.Map.map = map;

    return map;
};

djangoRef.Map.getActiveOverlays = function(){
    var retVal = [];
    for(var k in djangoRef.Map.overlays){
        k_layer = djangoRef.Map.overlays[k];
        if(djangoRef.Map.map.hasLayer(k_layer)){
            retVal.push(k_layer);
        }
    }
    return retVal;
}

djangoRef.Map.getOverlayByHandle = function(handle){
    return djangoRef.Map.overlays[handle];
};

djangoRef.Map.addOverlay = function(layer,layer_handle){
    overlays[layer_handle] = layer;
};

djangoRef.Map.deselectAllOverlays = function(){
    for(var k in djangoRef.Map.overlays){
        k_layer = djangoRef.Map.overlays[k];
        controlCapes.unSelectLayer(k_layer);
    }
};

djangoRef.Map.setState = function(state){
    djangoRef.Map.deselectAllOverlays();
    if(state.overlays && state.overlays.length > 0){
        for(var i = 0; i < state.overlays.length; i++){
            controlCapes.selectLayer( djangoRef.Map.overlays[state.overlays[i]] );
        }
    }
    if(state.base){
        controlCapes.selectLayer(eval(state.base));
    }
}

djangoRef.Map.getState = function(){
    var overlay_list = [];
    var base_layer = null;
    for (var k in djangoRef.Map.overlays){
        if(djangoRef.Map.map && djangoRef.Map.map.hasLayer(djangoRef.Map.overlays[k])){
            overlay_list.push(k);
        }
    }
    var base_layers = ['djangoRef.Map.roads','djangoRef.Map.satellite','djangoRef.Map.terrain','djangoRef.Map.hybrid','djangoRef.Map.osm'];
    for( var i = 0; i < base_layers.length; i++){
        if(djangoRef.Map.map && djangoRef.Map.map.hasLayer(eval(base_layers[i]))){
            base_layer = base_layers[i];
        }
    }
    var state = {
        overlays : overlay_list,
        base: base_layer
    };

    return state;
}

var register_overlays = function(overlays){
    for (var i = 0; i < overlays.length; i++){
        djangoRef.Map.overlays[overlays[i].name] = overlays[i].layer;
    }
}

var showGetFeatureInfo = function (err, latlng, content) {
    if (err) { console.log(err); return; } // do nothing if there's an error
    // Otherwise show the content in a popup, or something.
    L.popup({ maxWidth: 800}).setLatLng(latlng).setContent(content).openOn(map);
}

var getFeatureInfo = function(evt,querylayers){
    // Make an AJAX request to the server and hope for the best
    var url = getFeatureInfoUrl(evt.latlng,querylayers);
    $.ajax({
      url: url,
      success: function (data, status, xhr) {
        var err = typeof data === 'string' ? null : data;
        showGetFeatureInfo(err, evt.latlng, data);
      },
      error: function (xhr, status, error) {
        showGetFeatureInfo(error);
      }
    });
}

var getFeatureInfoUrl = function(latlng,querylayers){
    var point = map.latLngToContainerPoint(latlng, map.getZoom());
    var size = map.getSize();

    var params = {
      request: 'GetFeatureInfo',
      service: 'WMS',
      srs: 'EPSG:4326',
      styles: '',
      transparent: true,
      version: '1.1.1',
      format: 'image/jpeg',
      bbox: map.getBounds().toBBoxString(),
      height: size.y,
      width: size.x,
      layers: querylayers,
      query_layers: querylayers,
      info_format: 'text/html',
      feature_count: 10
    };

    params[params.version === '1.3.0' ? 'i' : 'x'] = point.x;
    params[params.version === '1.3.0' ? 'j' : 'y'] = point.y;

    return wms_url + L.Util.getParamString(params, wms_url, true);
};

})();
