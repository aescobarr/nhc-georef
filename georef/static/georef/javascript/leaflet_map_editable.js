$(document).ready(function() {
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	osm = new L.TileLayer(osmUrl, {minZoom: 2, maxZoom: 12, attribution: osmAttrib});

    map = new L.Map('map',{
        layers: [osm]
    });

	map.setView(new L.LatLng(40.58, -3.25),2);

	roads = L.gridLayer.googleMutant({
        type: 'roadmap' // valid values are 'roadmap', 'satellite', 'terrain' and 'hybrid'
    });

    satellite = L.gridLayer.googleMutant({
        type: 'satellite' // valid values are 'roadmap', 'satellite', 'terrain' and 'hybrid'
    });

    terrain = L.gridLayer.googleMutant({
        type: 'terrain' // valid values are 'roadmap', 'satellite', 'terrain' and 'hybrid'
    });

    hybrid = L.gridLayer.googleMutant({
        type: 'hybrid' // valid values are 'roadmap', 'satellite', 'terrain' and 'hybrid'
    });

    var baseMaps = [
        {
            groupName: "Open Street Maps",
            expanded: true,
            layers: {
                "Open Street Map": osm
            }
        },
        {
            groupName: "Google Base Maps",
            expanded: true,
            layers: {
                "Google roads": roads,
                "Google satellite": satellite,
                "Google terrain": terrain,
                "Google hybrid": hybrid
            }
        }
    ];

    //toponims =  L.tileLayer.wms('http://127.0.0.1:8080/geoserver/mzoologia/wms?', { layers: 'mzoologia:toponimsdarreraversio' , opacity: 0.5});
    toponims =  L.tileLayer.wms('http://127.0.0.1:8080/geoserver/mzoologia/wms?', { layers: 'mzoologia:toponimsdarreraversio' ,format: 'image/png', transparent: true});

    var overlays = [
        {
            groupName: "Toponims",
            expanded: true,
            layers: {
                "Darreres versions": toponims
            }
        }
    ];

    /*
    soybeans_sp.StyledLayerControl = {
		removable : true,
		visible : false
	}*/

	var options = {
		container_width 	: "180px",
		container_height    : "500px",
		container_maxHeight : "500px",
		group_maxHeight     : "120px",
		exclusive       	: false
	};

	var MyCustomMarker = L.Icon.extend({
        options: {
            shadowUrl: null,
            iconAnchor: new L.Point(12, 12),
            iconSize: new L.Point(24, 24),
            iconUrl: 'link/to/image.png'
        }
    });

    editableLayers = new L.FeatureGroup();
    map.addLayer(editableLayers);

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
            featureGroup: editableLayers, //REQUIRED!!
            remove: true
        }
    };

    var drawControl = new L.Control.Draw(draw_options);
    map.addControl(drawControl);

    /*control_layers = L.control.layers(baseMaps,overlays);
    control_layers.addTo(map);*/

    var control = L.Control.styledLayerControl(baseMaps, overlays, options);
	map.addControl(control);

	/*map.on(L.Draw.Event.CREATED, function (e) {
        var type = e.layerType,
            layer = e.layer;

        if (type === 'marker') {
            layer.bindPopup('A popup!');
        }

        editableLayers.addLayer(layer);
    });*/

    /*
    var jsonTest = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-14.941406,55.578345],[-1.230469,61.438767],[9.667969,55.178868],[-2.988281,44.339565],[-13.886719,50.958427],[-14.941406,55.578345]]]}}]};

    var geoJSONLayer = L.geoJson(jsonTest);
    geoJSONLayer.eachLayer(
        function(l){
            editableLayers.addLayer(l);
    });
    */
});