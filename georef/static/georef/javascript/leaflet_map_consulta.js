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
            groupName: 'Open Street Maps',
            expanded: true,
            layers: {
                'Open Street Map': osm
            }
        },
        {
            groupName: 'Google Base Maps',
            expanded: true,
            layers: {
                'Google roads': roads,
                'Google satellite': satellite,
                'Google terrain': terrain,
                'Google hybrid': hybrid
            }
        }
    ];

    var overlays = [];

    /*
    soybeans_sp.StyledLayerControl = {
		removable : true,
		visible : false
	}*/

    var options = {
        container_width 	: '180px',
        container_height    : '500px',
        container_maxHeight : '500px',
        group_maxHeight     : '120px',
        exclusive       	: false
    };

    /*
    var MyCustomMarker = L.Icon.extend({
        options: {
            shadowUrl: null,
            iconAnchor: new L.Point(12, 12),
            iconSize: new L.Point(24, 24),
            iconUrl: 'link/to/image.png'
        }
    });
    */

    var control = L.Control.styledLayerControl(baseMaps, overlays, options);
    map.addControl(control);

});