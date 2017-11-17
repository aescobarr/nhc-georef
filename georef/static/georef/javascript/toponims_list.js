$(document).ready(function() {
    table = $('#toponims_list').DataTable( {
        "ajax": {
            "url": _toponim_list_url,
            "dataType": 'json',
            "data": function(d){
                //d.mykey = "myvalue";
                //d.filtrejson = extreureJSONDeFiltre();
                var valorFiltre = getCookie("filtre_t");
                if(valorFiltre){
                    d.filtrejson = valorFiltre;
                }else{
                    d.filtrejson = extreureJSONDeFiltre();
                }
            }
        },
        "serverSide": true,
        "processing": true,
        //"language": opcions_llenguatge_catala,
        "pageLength": 25,
        "pagingType": "full_numbers",
        "bLengthChange": false,
        stateSave: true,
        "dom": '<"top"iflp<"clear">>rt<"bottom"iflp<"clear">>',
        stateSaveCallback: function(settings,data) {
            localStorage.setItem( 'DataTables_' + settings.sInstance, JSON.stringify(data) )
        },
        stateLoadCallback: function(settings) {
            return JSON.parse( localStorage.getItem( 'DataTables_' + settings.sInstance ) )
        },
        "columns": [
            { "data": "nom_str" }
            ,{ "data": "aquatic_str" }
            ,{ "data": "idtipustoponim.nom" }
        ],
        "columnDefs": [
            {
                "targets":0,
                "title": "Topònim"
            },
            {
                "targets":1,
                "title": "Aquàtic"
            },
            {
                "targets":2,
                "title": "Tipus"
            }
        ]
    } );

    /* LEAFLET */
    // create the tile layer with correct attribution


    /* OPENLAYERS */
    /*
    var styles = [
        'Road',
        'RoadOnDemand',
        'Aerial',
        'AerialWithLabels',
        'collinsBart',
        'ordnanceSurvey'
    ];

    var map = new ol.Map({
        target: 'map',
        layers: [
          new ol.layer.Tile({
            source: new ol.source.TileImage({
                url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attributions: [
                    new ol.Attribution({
                        html: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
                })
                ]
            })
          })
        ],
        view: new ol.View({
          center: ol.proj.fromLonLat([-2.285156,39.077775]),
          zoom: 6
        })
    });*/
});