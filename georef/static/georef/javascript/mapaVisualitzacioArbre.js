var permetUnCheck = false;
var testLayer;
var txtDefaultOLSpanish = {'baseLayer': "Cartografía de referencia",'overlays':"Capas"};
var txtDefaultOLCatalan = {'baseLayer': "Cartografia de referència",'overlays':"Capes"};
var map, vectors, controls;
var info_ctrl;
//, layersSwitch;
//var pointLayer,lineLayer;
var numMaximElementsDigitalitzar = 100;
var taulaConsultaCarto;
var esEditableMapaCarto = false;
var esEditableRectangleMapaCarto = false;
function initMapa(taula){
    taulaConsultaCarto = taula;
    OpenLayers.Lang.es = txtDefaultOLSpanish;
    OpenLayers.Lang.ca = txtDefaultOLCatalan;
    OpenLayers.Lang.setCode('ca');
    var optionsMap = {
        //projection: new OpenLayers.Projection("EPSG:900913"),
        projection: new OpenLayers.Projection("EPSG:3857"),
        displayProjection: new OpenLayers.Projection("EPSG:4326"),
        units: "m",
        numZoomLevels: 18,
        maxResolution: 'auto',
        maxExtent: new OpenLayers.Bounds(-180, -90, 180, 90),
        controls:[new OpenLayers.Control.Navigation()]
    };
    map = new OpenLayers.Map('map',optionsMap);

    var baseLayers = inicialitzaBaseLayersJSON(jsonData);
//    var baseLayers = new Array();
    
//    var osmOverlay = new OpenLayers.Layer.OSM("OpenCycleMap",
//      ["http://a.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
//       "http://b.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
//       "http://c.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png"]);

//    var osmOverlay = new OpenLayers.Layer.OSM("OpenCycleMap",
//      ["http://a.tile.openstreetmap.org/${z}/${x}/${y}.png",
//       "http://b.tile.openstreetmap.org/${z}/${x}/${y}.png",
//       "http://c.tile.openstreetmap.org/${z}/${x}/${y}.png"]);

//    var osmOverlay = new OpenLayers.Layer.OSM();
//      
//    baseLayers.push(osmOverlay);

    OpenLayers.Feature.Vector.style['default']['strokeWidth'] ='2';


    vectors = new OpenLayers.Layer.Vector("digitalització", {
                projection: new OpenLayers.Projection("EPSG:4326")                
            });


    var removeOptions = {
                clickout: true,
                onSelect: featureRemove,
                toggle: false,
                multiple: false,
                hover: false
            };

    var funcioFinalDigitalitzacio = function(){
        var maxElementsSobrepassat = numMaximElementsDigitalitzar<=vectors.features.length;
        if(maxElementsSobrepassat){
            toggleControl('moure');
        }
    }

    var controlPoligon = new OpenLayers.Control.DrawFeature(vectors,
                                OpenLayers.Handler.Polygon);

    var controlPunt = new OpenLayers.Control.DrawFeature(vectors,
                                OpenLayers.Handler.Point);


    var controlLinia = new OpenLayers.Control.DrawFeature(vectors,
                                OpenLayers.Handler.Path);



    var controlRegular = new OpenLayers.Control.DrawFeature(vectors,
                            OpenLayers.Handler.RegularPolygon,
                            {handlerOptions: {sides: 4,
                                              irregular: true,finalize:funcioFinalDigitalitzacio}}
                             );
                                 
    var attribution = new OpenLayers.Control.Attribution();

    info_bubble = new OpenLayers.Control.WMSGetFeatureInfo({
        url: 'http://'+urlServidor+'/geoserver/wms',
        title: 'Identify features by clicking',
        queryVisible: true,
        infoFormat: 'text/html',
        div : OpenLayers.Util.getElement('tabinfo'),
        eventListeners: {
            getfeatureinfo: function(event) {
                if(event.text.split('_#_').length>1){
                    map.addPopup(
                        new OpenLayers.Popup.FramedCloud(
                            "chicken",
                            map.getLonLatFromPixel(event.xy),
                            null,
                            getFilaInfoText(event),
                            null,
                            true
                            )
                    );
                }
            }
        }
    });

    info_ctrl = new OpenLayers.Control.WMSGetFeatureInfo({
        //url: 'http://'+urlServidor+'/geoserver/wms',
        //url: 'http://sitmun.diba.cat/wms/servlet/SITXELL',
        title: 'Identify features by clicking',
        drillDown: true,
        queryVisible: true,
        eventListeners: {
            getfeatureinfo: function(event) {
                var elem = document.getElementById('tabinfo');
                elem.innerHTML = event.text;
                $( "#tabsctrlmapa" ).tabs('select',2);
            }
        }
    });
    
    info_ctrl.responses  = [];
    info_ctrl.handleResponse=function(xy, request) {        
        var doc = request.responseXML;
        if(!doc || !doc.documentElement) {   
            doc = request.responseText; 
        }
        var features = this.format.read(doc);
        if (this.drillDown === false) {
            this.triggerGetFeatureInfo(request, xy, features);
        } else {
            this._requestCount++;
            this._features = (this._features || []).concat(features);
            if( this._numRequests > 1){
                //if the num of RQ, (I mean more than 1 resource ), i put the Request in array, this is for maybe in a future i could be need other properties or methods from RQ, i dont know.
                this.responses.push(request);
            }else{
                this.responses = request;
            }
            if (this._requestCount === this._numRequests) {
            //here i change the code....
            //this.triggerGetFeatureInfo(request, xy, this._features.concat());
                this.triggerGetFeatureInfo(this.responses, xy, this._features.concat());
                delete this._features;
                delete this._requestCount;
                delete this._numRequests;
                // I Adding this when the all info is done 4 reboot
                this.responses=[];
            }
        }
    }
    
    info_ctrl.triggerGetFeatureInfo= function( request , xy , features) {
        if( request instanceof Array ){
            text_rq = '';
            for(i in request ){
                text_rq += request[i].responseText;
            }
        }else{
            text_rq = request.responseText;
        }
        this.events.triggerEvent("getfeatureinfo", {
            //text: request.responseText,
            text : text_rq,
            features: features,
            request: request,
            xy: xy
        });
        // Reset the cursor.
        OpenLayers.Element.removeClass(this.map.viewPortDiv, "olCursorWait");
    }



    controls = {
        point: controlPunt,
        line: controlLinia,
        polygon: controlPoligon,
        regular: controlRegular,
        attribution: attribution,
        zoom: new OpenLayers.Control.ZoomBox({alwaysZoom:true}),
        remove: new OpenLayers.Control.SelectFeature(vectors,removeOptions),
        info: info_ctrl
    };


    map.addControl(new OpenLayers.Control.ScaleLine());
    map.addControl(new OpenLayers.Control.MousePosition({'div':OpenLayers.Util.getElement('coordenades')
        ,'numDigits':6}));

    map.addControl(new OpenLayers.Control.PanZoomBar({'zoomWorldIcon':true}));

    for(var key in controls) {
        map.addControl(controls[key]);
        controls[key].deactivate();
    }
    
    map.addLayers(baseLayers);
    
    if(esEditableMapaCarto || esEditableRectangleMapaCarto){
        map.addLayers([vectors]);
    }
    
    
    var mapOverview = new OpenLayers.Layer.WMS(
            "OpenLayers WMS",
            "http://vmap0.tiles.osgeo.org/wms/vmap0",
            {layers: 'basic',tileOptions: {maxGetUrlLength: 1}, transitionEffect: 'resize'}
        );

    var controlOverviewOptions = {
        layers: [mapOverview],
        div: document.getElementById('panellSituacio')
    }

    var overview = new OpenLayers.Control.OverviewMap(controlOverviewOptions);

    map.addControl(overview);
    map.zoomToMaxExtent();

//    map.zoomToMaxExtent();
    map.events.register('zoomend', null, function() {
        if(typeof canviCentroide == 'function'){
            canviCentroide();
        }
    });        
}

function consultaNomesArabidopsis(){
    var capaArabidopsis = map.getLayersByName('dormant_arabidopsis_punts')[0];
    info_ctrl.layers = [capaArabidopsis];
}


function inicialitzaBaseLayersJSON(jsonData){
    var retorn = new Array();
    for(var i = 0; i < jsonData.data.length; i++){
        //Grups de capes
        var grup_i = jsonData.data[i];
        var capa;
        if(grup_i.attr.id=="baselayers"){
            var children = grup_i.children;
            for(var j = 0; j < children.length; j++ ){
                var child_j = children[j];
                if(child_j.attr.layertype=="google"){
                    capa = inicialitzaCapaGoogle(grup_i.children[j]);
                }else if(child_j.attr.layertype=="wms"){
                    capa = createLayerWMS(child_j.attr.id,child_j.attr.idlayergs,
                    child_j.attr.url);
                }else if(child_j.attr.layertype=="osm"){
                    capa = new OpenLayers.Layer.OSM();
                    capa.setName(child_j.attr.id);
                }
                retorn.push(capa);
            }
        }
    }
    return retorn;
}

function createLayerWMS(idCapa,idCapaServidor,urlServidorWms){
    var capa = new OpenLayers.Layer.WMS(
		    idCapa, urlServidorWms,
			{layers: idCapaServidor, format:"image/jpeg",
            exceptions: 'INIMAGE'},/* exceptions:"application/vnd.ogc.se_xml"},*/
			{buffer:0, transitionEffect:'resize', resolutions: [550,275,100,50,25,10,5,2,1,0.5],
                            tileOptions: {maxGetUrlLength: 1}, transitionEffect: 'resize'}
		  );
    return capa;
}

function createLayerWMSAlt(idCapa,idCapaServidor,url){
    var capa;
    capa = new OpenLayers.Layer.WMS(
        idCapa,
        url,
        {
            layers: idCapaServidor,
            styles: '',
            transparent: 'true',
            format: 'image/png',
            width: '800',
            height: '600',
            tiled: 'true',exceptions: 'INIMAGE'
        },
        {buffer: 0, displayOutsideMaxExtent: true,transitionEffect: 'resize'}
    );
    capa.setOpacity(0.8);
    return capa;
}

function createLayerSenseFiltreSufixUrl(idCapa,idCapaGeoServer,sufixUrl){
    var capa;
    capa = new OpenLayers.Layer.WMS(
        idCapa,
        "http://" + urlServidor + sufixUrl,
        {
            layers: idCapaGeoServer,
            styles: '',
            transparent: 'true',
            format: 'image/png',
            width: '800',
            height: '600',
            tiled: 'true',exceptions: 'INIMAGE'
        },
        {buffer: 0, displayOutsideMaxExtent: true,
            tileOptions: {maxGetUrlLength: 1}, transitionEffect: 'resize'}
    );
    capa.setOpacity(0.8);
    return capa;
}

function createLayerSenseFiltre(idCapa,idCapaGeoServer){
    var capa;
    capa = new OpenLayers.Layer.WMS(
        idCapa,
        "http://" + urlServidor + "/geoserver/wms",
        {
            layers: idCapaGeoServer,
            styles: '',
            transparent: 'true',
            format: 'image/png',
            width: '800',
            height: '600',
            tiled: 'true',exceptions: 'INIMAGE'
        },
        {buffer: 0, displayOutsideMaxExtent: true,
            tileOptions: {maxGetUrlLength: 1}, transitionEffect: 'resize'}
    );
    capa.setOpacity(0.8);
    return capa;
}

function aplicaFiltreACapa(idCapa, cql){
    var layers;
    if(map){
        layers = map.getLayersByName(idCapa);
        if(layers){
            var layer = layers[0];
            if(layer){
                var filterParams;
                if(cql){
                    filterParams = {
                        cql_filter: cql
                    };
                }else{
                    filterParams = {
                        cql_filter: null
                    };
                }
                layer.mergeNewParams(filterParams);
                layer.redraw(true);
            }
        }
    }
}

function aplicaFiltreACapaFormatCQL(idCapa, cql){
    var layers;
    if(map){
        layers = map.getLayersByName(idCapa);
        if(layers){
            var layer = layers[0];
            if(layer){
                var filterParams;
                if(cql){
                    filterParams = {
                        cql_filter: new OpenLayers.Format.CQL().write(cql) 
                    };
                }else{
                    filterParams = {
                        cql_filter: null
                    };
                }
                layer.mergeNewParams(filterParams);
                layer.redraw(true);
            }
        }
    }
}

function processaNode(clau){
    var capa;
    if(clau.attr){
        if(clau.attr.id && (clau.attr.idlayergs || clau.attr.baseURL)){
            if(clau.attr.sufixurl){
                capa = createLayerSenseFiltreSufixUrl(clau.attr.id,clau.attr.idlayergs,clau.attr.sufixurl);
            }else if(clau.attr.baseURL){
                capa = createLayerWMSAlt(clau.attr.id,clau.attr.id,clau.attr.baseURL);                
            }else{
                capa = createLayerSenseFiltre(clau.attr.id,clau.attr.idlayergs);
            }            
            capa.setVisibility(false);
            map.addLayer(capa);
        }
    }
}

function recorreJSONRecursivament(o,func) {
    for (var i in o) {
        func.apply(this,[o]);
        if (typeof(o[i])=="object") {
            recorreJSONRecursivament(o[i],func);
        }
    }
}

function inicialitzaOverlaysJSONRecursivament(jsonData){
    recorreJSONRecursivament(jsonData,processaNode);
    if(vectors!=null)
        vectors.setZIndex(1000);
}

function inicialitzaCapaGoogle(jsonData){
    var options;
    if(jsonData.attr.numZoomLevels){
        options =   {
                        type: jsonData.attr.type
                        ,numZoomLevels: parseInt(jsonData.attr.numZoomLevels)
                    }
    }else{
        options =   {
                        type: jsonData.attr.type
                        ,maxZoomLevel:15
                    }
    }
    var layer = new OpenLayers.Layer.Google(
        jsonData.attr.data,
        options
    );
    layer.setName(jsonData.attr.id);
    return layer;
}

function featureRemove(feature) {
            var x = confirm(txtOpenlayers.MSG_ELIMINAR);
            if (x==true) {
                vectors.removeFeatures(feature);
            }
        }

function initAddPolygon(){

}

function comprovacioPreAfegir(x,y){
    return comprovacioAmbitCoordenada(x,y);
}

function comprovacioAmbitCoordenada(x,y){
    var bounds = map.maxExtent;
    if( x < bounds.left || x > bounds.right || y < bounds.bottom || y > bounds.top ){
        alert("La coordenada " + x + "," + y + " cau fora de l'àmbit del mapa.");
        return false;
    }
    return true;
}

function toggleControl(element) {
    for(key in controls) {
        var control = controls[key];
        if(element == key && element=='point') {
            var maxElementsSobrepassat = numMaximElementsDigitalitzar<=vectors.features.length;
            if(maxElementsSobrepassat){
                alert(txtOpenlayers.MSG_ERROR_MASSA_ELEMENTS_DIGITALITZATS);
            }else{
                var divcoords = document.getElementById('coordenadesPunt');
                if(divcoords!=null)
                    divcoords.style.display='inline';
                divcoords = document.getElementById('coordenadesRectangle');
                if(divcoords!=null)
                    divcoords.style.display='none';
                control.activate();
            }
        } else if(element == key && element=='regular') {
            maxElementsSobrepassat = numMaximElementsDigitalitzar<=vectors.features.length;
            if(maxElementsSobrepassat){
                alert(txtOpenlayers.MSG_ERROR_MASSA_ELEMENTS_DIGITALITZATS);
            }else{
                divcoords = document.getElementById('coordenadesRectangle');
                if(divcoords!=null)
                    divcoords.style.display='inline';
                divcoords = document.getElementById('coordenadesPunt');
                if(divcoords!=null)
                    divcoords.style.display='none';
                control.activate();
            }
        } else if(element == key) {
            divcoords = document.getElementById('coordenadesPunt');
            if(divcoords!=null)
                divcoords.style.display='none';
            divcoords = document.getElementById('coordenadesRectangle');
            if(divcoords!=null)
                divcoords.style.display='none';
            control.activate();
        } else if(element=='moure') {
            divcoords = document.getElementById('coordenadesPunt');
            if(divcoords!=null)
                divcoords.style.display='none';
            divcoords = document.getElementById('coordenadesRectangle');
            if(divcoords!=null)
                divcoords.style.display='none';
            control.deactivate();
        } else {
            control.deactivate();
        }
    }
}

function esborrarSeleccionats(){
    var seleccionats = vectors.selectedFeatures;
    vectors.removeFeatures(seleccionats);
}

function getWKTDeObjectesDigitalitzats(){
    var digits = vectors.features;
    var geoWKT = new OpenLayers.Format.WKT( {externalProjection: map.displayProjection,
 	            internalProjection: map.projection
    });
    return geoWKT.write(digits);
}

function mostrarWTK(wkt){
    var geoWKT = new OpenLayers.Format.WKT({
 	            externalProjection: map.displayProjection,
 	            internalProjection: map.projection                    
 	        });    
    var feats = geoWKT.read(wkt);
    if(feats && hihaCoordenadesNaN(feats)){
        alert(txtOpenlayers.MSG_ERRORIMPORTANTVEC);
    }else if(feats){
        vectors.addFeatures(feats);
    }else{
        clearFeaturesMapa();
    }
}

function hihaCoordenadesNaN(feats){
    for(i=0;i<feats.length;i++){
        if(feats[i].geometry.toString().indexOf('NaN')>-1){
            return true;
        }
    }    
    return false;
}

function centrarMapaADigitalitzacio(){
    var bounds = vectors.getDataExtent();
    if(bounds!=null){
        map.zoomToExtent(bounds);        
    }else{
        map.zoomToMaxExtent();
    }
}

function clearFeaturesMapa(){
    vectors.removeFeatures(vectors.features);
}

function afegirCapa(capaNova){
    if(map!=null)
        map.addLayer(capaNova);
}

function eliminarCapa(capaNova){
    if(map!=null)
        map.removeLayer(capaNova,null);
}

function eliminarCapaPerNom(nomCapa){
    var layers = map.getLayersByName(nomCapa);
    for(var layerIndex = 0; layerIndex < layers.length; layerIndex++){
        map.removeLayer(layers[layerIndex]);
    }
}

var mapa;
var pareMapa;
var hideMapa;
var pareAmagarMapa;
var iniciat = false;
function veureAmagarMapa(tamany){
    if(mapa==null){
        mapa = document.getElementById('map');
        pareMapa = mapa.parentNode;
        pareMapa.removeChild(mapa);
    }else{
        if(tamany!=""){
            mapa.setAttribute("class",tamany);
        }
        pareMapa.appendChild(mapa);
        pareMapa = null;
        mapa = null;
        if(!iniciat){
            map.zoomToMaxExtent();
            iniciat = true;
        }
    }
}

function amagarMapa(){
    if(mapa==null){
        mapa = document.getElementById('map');
        pareMapa = mapa.parentNode;
    }
    pareMapa.removeChild(mapa);
    hideMapa = document.getElementById('hidemap');
    if(hideMapa!=null){
        pareAmagarMapa = hideMapa.parentNode;
        pareAmagarMapa.removeChild(hideMapa);
    }
}

function veureMapa(tamany){
    if(mapa==null){
        mapa = document.getElementById('map');
        pareMapa = mapa.parentNode;
    }
    if(tamany!=""){
        mapa.setAttribute("class",tamany);
    }
    pareMapa.appendChild(mapa);
    map.zoomToMaxExtent();
    if(pareAmagarMapa!=null && document.getElementById('hidemap')==null){
        pareAmagarMapa.appendChild(hideMapa);
    }
}

function getElementsDigitalitzats(){
    return vectors.features.length;
}

function getFilaInfoText(event){
    var geoserver = "\"" + event.text + "\"";
    var html = parseGeoserverHTML(geoserver,taulaConsultaCarto);
    return html;
}

function parseGeoserverHTML(geoserver,taulaEntrada){
    var taules = extreureTaules(geoserver,taulaEntrada);
    html = "<div>";
    for(i=0;i<taules.length;i++){
        html = html + taules[i];
    }
    html = html + "</div>";
    return html;
}

function extreureTaules(geoserver,taulaEntrada){
    var cadenesAmbTaules = geoserver.split('_#_');
    var numValides = contarCadenesValides(cadenesAmbTaules);
    var taules = new Array(numValides);
    var bones = 0;
    for(var i=1;i<cadenesAmbTaules.length;i++){
        var taula = extreureTaula(cadenesAmbTaules[i],taulaEntrada);
        if(taula!=null){
            taules[bones] = taula;
            bones++;
        }
    }
    return taules;
}

function contarCadenesValides(cadenes){
    var numValides = 0;
    for(var i=1;i<cadenes.length;i++){
        if(cadenes[i]!=null && cadenes[i]!=''){
            numValides++;
        }
    }
    return numValides;
}

function extreureTaula(geoserver,taulaEntrada){
    if(geoserver==null || geoserver==''){
        return null;
    }
    var nomTaula = geoserver.substr(0,geoserver.indexOf('_$_'));
    var contingutTaula = geoserver.substr(geoserver.indexOf('_$_')+3);
    var html = "<table class='estil1'><thead>";
    var titols = contingutTaula.substr(0,contingutTaula.indexOf('_&_'));
    var camps = contingutTaula.substr(contingutTaula.indexOf('_&_')+3);
    var numCols = contarNumeroColumnes(titols);
    html = html + extreureTitolsColumnes(titols,taulaEntrada[nomTaula]);
    html = html + "</thead><tbody>";
    html = html + extreureCampsColumnes(numCols,camps,taulaEntrada[nomTaula]);
    html = html + "</tbody></table>";
    return html;
}


function contarNumeroColumnes(geoserver){
    if(geoserver==null || geoserver==''){
        return null;
    }
    var contingutTaula = geoserver.split('_$_');
    return contingutTaula.length;
}

function extreureTitolsColumnes(geoserver,taulaEntrada){
    if(geoserver==null || geoserver==''){
        return null;
    }
    var html = "<tr>";
    for(var i=0;i<taulaEntrada[1].length;i++){
        html = html + "<th>" + taulaEntrada[1][i][1] + "</th>";
    }
    html = html + "</tr>";
    return html;
}

function extreureCampsColumnes(numCols,geoserver,taulaEntrada){
    if(geoserver==null || geoserver==''){
        return null;
    }
    var contingutTaula = geoserver.split('_&_');
    var html = "";
    for(var k=0;k<contingutTaula.length/numCols;k++){
        for(var i=0;i<taulaEntrada[1].length;i++){
            if(i%numCols==0){
                html = html + "<tr>";
            }
            html = html + "<td>";
            if(taulaEntrada[0]!=null && taulaEntrada[0].length>0){
                html = html + "<a href='#' onclick=\"javascript:"+taulaEntrada[0][0]+"(";
                for(var j=0;j<taulaEntrada[0][1].length;j++){
                    html = html + "'" + netejaCadena(contingutTaula[k*numCols + taulaEntrada[0][1][j]]) + "'";
                    if(j<taulaEntrada[0][1].length-1){
                        html = html + ",";
                    }
                }
                html = html + ")\">";
            }
            html = html + contingutTaula[k*numCols + taulaEntrada[1][i][0]];
            if(taulaEntrada[0]!=null && taulaEntrada[0].length>0){
                html = html + "</a>";
            }
            html = html  + "</td>";
            if(i%numCols==numCols-1){
                html = html + "</tr>";
            }
        }
    }
    return html;
}

function netejaCadena(s) {
    var r = "";
    for (var i=0; i < s.length; i++) {
        if (s.charAt(i) != '\n' &&
            s.charAt(i) != '\r' &&
            s.charAt(i) != '\t' &&
            s.charAt(i) != ' ') {
            r += s.charAt(i);
        }
    }
    return r;
}

/** Part de les capes **/


function initCaixaCapa(
    id_li,
    estilCssCaixa,
    idIcona,
    idCapaGeoServer,
    etiquetaCapaACaixa,
    ipServidorGeoServer,
    veureKML,
    veureSHP
    ){
    var html;
    html = "<div class=\"botons_capa\">";
    if(veureKML){
    //html = html + "<a class=\"kml\" href=\"http://" + ipServidorGeoServer + "/wms/geoserver/wms/kml?layers=" + idCapaGeoServer + "\" target=\"_blank\"></a>";
    html = html + "<a class=\"kml\" href=\"http://" + ipServidorGeoServer + "/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=" + idCapaGeoServer + "&styles=&bbox=246809.50679615702,4429945.3655678565,531814.7343779552,4804968.5619192235&width=389&height=512&srs=EPSG:23031&format=application/vnd.google-earth.kml+xml\" target=\"_blank\"></a>";
    }
    if(veureSHP){
        //html = html + "<a class=\"veure_shape\" href=\"http://" + ipServidorGeoServer + "/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=" + idCapaGeoServer + "&styles=&bbox=246809.50679615702,4429945.3655678565,531814.7343779552,4804968.5619192235&width=389&height=512&srs=EPSG:23031&format=application/vnd.google-earth.kml+xml\" target=\"_blank\"></a>";
    html = html + "<a class=\"veure_shape\" href=\"http://" +ipServidorGeoServer+"/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName="+idCapaGeoServer+"&outputFormat=SHAPE-ZIP\"  target=\"_blank\"></a>";
    }
    html = html + "<a id=\"" + idIcona + "\" class=\"noveurecapa\" href=\"#\" onclick=\"javascript:mostrarAmagarCapa('" + idIcona + "','" + id_li + "');return false;\"></a>";
    html = html + "</div>";
    html = html + "<div class=\"titol_capa\">";
    html = html + etiquetaCapaACaixa;
    html = html + "</div>";

    var contenidorCapes = document.getElementById('llistacapes');
    var nouLi = document.createElement('li');
    nouLi.setAttribute("id", id_li);
    nouLi.setAttribute("class", "capa " + estilCssCaixa);
    nouLi.innerHTML = html;
    contenidorCapes.appendChild(nouLi);
}

function afegirCapaASwitch(
    capaAAfegir,
    id_li,
    estilCssCaixa,
    idIcona,
    idCapaGeoServer,
    etiquetaCapaACaixa,
    ipServidorGeoServer,
    veureKML,
    veureSHP
    ){
    map.addLayer(capaAAfegir);
    initCaixaCapa(
        id_li,
        estilCssCaixa,
        idIcona,
        idCapaGeoServer,
        etiquetaCapaACaixa,
        ipServidorGeoServer,
        veureKML,
        veureSHP
        );
     var icona = document.getElementById(idIcona);
     obreUll(true,icona);
}

function creaCapaASwitch(
    id_li,
    transparencia,
    estilCssCaixa,
    idIcona,
    idCapaGeoServer,
    etiquetaCapaACaixa,
    ipServidorGeoServer,
    format,
    veureKML,
    formatExcepcions
    ){
    var capa = new OpenLayers.Layer.WMS(
        id_li, ipServidorGeoServer,
        {
            layers: idCapaGeoServer,
            styles: '',
            transparent: 'true',
            format: format,
            width: '800',
            height: '600',
            tiled: 'true',
            exceptions: 'INIMAGE'
        },
        {
            buffer: 0
        ,tileOptions: {maxGetUrlLength: 1}, transitionEffect: 'resize'}
        );
    if(formatExcepcions!=null){
        capa = new OpenLayers.Layer.WMS(
        id_li, ipServidorGeoServer,
        {
            layers: idCapaGeoServer,
            styles: '',
            transparent: 'true',
            format: format,
            exceptions: formatExcepcions,
            width: '800',
            height: '600',
            tiled: 'true'
        },
        {
            buffer: 0
        ,tileOptions: {maxGetUrlLength: 1}, transitionEffect: 'resize'}
        );
    }
    capa.setOpacity(transparencia);
    capa.setVisibility(false);
    map.addLayer(capa);
    initCaixaCapa(
        id_li,
        estilCssCaixa,
        idIcona,
        idCapaGeoServer,
        etiquetaCapaACaixa,
        ipServidorGeoServer,
        veureKML,
        false
        );
}


function actualitzaPosicioCapaMap(idControl,delta){
    var capa = getCapaDeIdLlista(idControl);
    if(capa){
        map.raiseLayer(capa,delta);
    }

}

function pujaControl(idcontrol){
    var control = document.getElementById(idcontrol);
    var clonControl = control.cloneNode(true);
    var contenidorControl = document.getElementById('llistacapes');
    var controlAnterior = YAHOO.util.Dom.getPreviousSibling(idcontrol);
    if(controlAnterior){
        contenidorControl.removeChild(control);
        contenidorControl.insertBefore(clonControl, controlAnterior);
    }
    ajustaOrdreLayers();
}

function baixaControl(idcontrol){
    var control = document.getElementById(idcontrol);
    var clonControl = control.cloneNode(true);
    var contenidorControl = document.getElementById('llistacapes');
    var controlSeguent = YAHOO.util.Dom.getNextSibling(idcontrol);
    if(controlSeguent){
        contenidorControl.removeChild(control);
        contenidorControl.insertBefore(clonControl, controlSeguent.nextSibling);
    }
    ajustaOrdreLayers();
}

function ajustaOrdreLayers(){
    var contenidorControl = document.getElementById('llistacapes');
    var nodeList = YAHOO.util.Dom.getChildren(contenidorControl);
    var llistaCapes = new Array();
    var index = 0;
    for(var i = nodeList.length-1; i >= 0; i--){
        var capa = getCapaDeIdLlista(nodeList[i].id);
        if(capa){
            if(capa.getVisibility()){
                llistaCapes[index] = capa;
                index++;
            }
        }
    }
    var posicioLayer = 3;
    for(i = 0; i < llistaCapes.length; i++){
        map.setLayerIndex(llistaCapes[i],posicioLayer);
        posicioLayer++;
    }
}

function getCapaDeIdLlista(idLlista){
    if(map)
        return map.getLayersByName(idLlista)[0];
    return null;
}

function obreUll(actiu,iconaVis){
    if(actiu){
        iconaVis.setAttribute("class", "veurecapa");
    }else{
        iconaVis.setAttribute("class", "noveurecapa");
    }
}

function mostrarAmagarCapa(idIcona, nomCapa){
    var iconaVis = document.getElementById(idIcona);
    var capa = getCapaDeIdLlista(nomCapa);
    if(capa!=null){
        if(capa.getVisibility()){
            capa.setVisibility(false);
            obreUll(false,iconaVis);
        }else{
            capa.setVisibility(true);
            obreUll(true,iconaVis);
        }
    }
    ajustaOrdreLayers();
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function digitalitzarRectangle(x0,y0,x1,y1,sistemaReferenciaLatLong){
    if(x0==null || x0=='' || y0==null || y0=='' ||
       x1==null || x1=='' || y1==null || y1=='' ||
        !validarCoordenadesSistemaReferencia(x0,y0,sistemaReferenciaLatLong) ||
        !validarCoordenadesSistemaReferencia(x1,y1,sistemaReferenciaLatLong)){
        alert(txtOpenlayers.MSG_COORDENADES_INCORRECTES);
    }else{
//        var textPunt = "GEOMETRYCOLLECTION (LINESTRING ("+x0+" "+y0+","+x1+" "+y1+"))";
        var textPunt = "GEOMETRYCOLLECTION (POLYGON(("+x0+" "+y0+", "+x1+" "+y0+", "+x1+" "+y1+", "+x0+" "+y1+", "+x0+" "+y0+")))";

        mostrarWTK(textPunt);
//        var bounds = new OpenLayers.Bounds(-10, 50, 5, 60);
//        var box = new OpenLayers.Feature.Vector(bounds.toGeometry());
//        vectors.addFeatures(box);
    }
}

function digitalitzarPoligonGeodesicACapa(x,y,capa,radi){
    var origin = new OpenLayers.Geometry.Point(x,y);
    var p = createGeodesicPolygon(origin, radi, 20, 18, map.projection);
    var pol = new OpenLayers.Feature.Vector(p);
    capa.addFeatures(pol);
    return p;
}

function digitalitzarPuntACapa(x,y,sistemaReferenciaLatLong,capa){
    if(x==null || x=='' || y==null || y=='' || !validarCoordenadesSistemaReferencia(x,y,sistemaReferenciaLatLong)){
        alert(txtOpenlayers.MSG_COORDENADES_INCORRECTES);
    }else{
        var textPunt = "GEOMETRYCOLLECTION (POINT ("+x+" "+y+"))";
        var geoWKT = new OpenLayers.Format.WKT({
 	            externalProjection: map.displayProjection,
 	            internalProjection: map.projection
 	        });
        var feats = geoWKT.read(textPunt);
        if(feats){
            capa.addFeatures(feats);
        }else{
            capa.removeFeatures(capa.features);
        }
    }
}


function digitalitzarPunt(x,y,sistemaReferenciaLatLong){
    if(x==null || x=='' || y==null || y=='' || !validarCoordenadesSistemaReferencia(x,y,sistemaReferenciaLatLong)){
        alert(txtOpenlayers.MSG_COORDENADES_INCORRECTES);
    }else{
        var textPunt = "GEOMETRYCOLLECTION (POINT ("+x+" "+y+"))";
        mostrarWTK(textPunt);
    }
}

function digitalitzarCercle(x,y,radi,sistemaReferenciaLatLong){
    if(x==null || x=='' || y==null || y=='' || !validarCoordenadesSistemaReferencia(x,y,sistemaReferenciaLatLong) || radi<0){
        alert(txtOpenlayers.MSG_COORDENADES_INCORRECTES);
    }else{
//        var textPunt = "GEOMETRYCOLLECTION (POINT ("+x+" "+y+"))";
//        alert(textPunt);
//        mostrarWTK(textPunt);

//        var render = OpenLayers.Renderer.VML();
//        var punt = new OpenLayers.Geometry.Point(
//                        x,y
//                    );
//        render.drawCircle(map,punt,radi);
        var points = new OpenLayers.Layer.Vector("Points", {
            externalProjection: map.displayProjection,
 	            internalProjection: map.projection//,
//                styleMap: myStyles,
//                rendererOptions: {zIndexing: true}
            });

var features = new Array(1);
        var proj = new OpenLayers.Projection("EPSG:4326");
        var poli = dibuixarBuffer (x,y, radi*100, 60, proj);

features[0] = poli;
            points.addFeatures(features);
            map.addLayers([points]);

//        var features = new Array(1);
//
//        features[0] = new OpenLayers.Feature.Vector(
//                    new OpenLayers.Geometry.Point(
//                        x,y
//                    )
//                        , {
//                        type: radi
//                    }
//                );
//
//        var myStyles = new OpenLayers.StyleMap({
//                "default": new OpenLayers.Style({
//                    pointRadius: "${type}", // sized according to type attribute
//                    fillColor: "#ffcc66",
//                    strokeColor: "#ff9933",
//                    strokeWidth: 2,
//                    graphicZIndex: 1
//                }),
//                "select": new OpenLayers.Style({
//                    fillColor: "#66ccff",
//                    strokeColor: "#3399ff",
//                    graphicZIndex: 2
//                })
//            });
//
//        var points = new OpenLayers.Layer.Vector("Points", {
//            externalProjection: map.displayProjection,
// 	            internalProjection: map.projection,
//                styleMap: myStyles,
//                rendererOptions: {zIndexing: true}
//            });
//            points.addFeatures(features);
//            map.addLayers([points]);
    }
}

function dibuixarBuffer (x,y, radius, sides, projection){

    if (projection.getCode() !== "EPSG:4326") {
        origin.transform(projection, new OpenLayers.Projection("EPSG:4326"));
    }
    var latlon = new OpenLayers.LonLat(x, y);

    var angle;
    var new_lonlat, geom_point;
    var points = [];

    for (var i = 0; i < sides; i++) {
        angle = (i * 360 / sides);// + rotation;
        new_lonlat = OpenLayers.Util.destinationVincenty(latlon, angle, radius);
        new_lonlat.transform(new OpenLayers.Projection("EPSG:4326"), projection);
        geom_point = new OpenLayers.Geometry.Point(new_lonlat.lon, new_lonlat.lat);
        points.push(geom_point);
    }
    var ring = new OpenLayers.Geometry.LinearRing(points);
    return new OpenLayers.Geometry.Polygon([ring]);
}

function validarCoordenadesLatLong(x,y){
    return !(x<-180 || x>180 || y<-90 || y>90 || isNaN(x) || isNaN(y));
}

function validarCoordenadesUTM(x,y){
    return !(isNaN(x) || isNaN(y));
}



function validarCoordenadesSistemaReferencia(x,y,sistemaReferenciaLatLong){
    if(sistemaReferenciaLatLong==true){
        return validarCoordenadesLatLong(x,y);
    }else{
        return validarCoordenadesUTM(x,y);
    }
}

function setEsEditableMapaCarto(b){
    var divEdicio = document.getElementById('controlsEdicio');
    if(b){
        divEdicio.style.visibility = "visible";
    }else{
        divEdicio.style.visibility = "collapse";
    }
}

function setEsEditableRectangleMapaCarto(b){
    var divEdicio = document.getElementById('controlsEdicioRectangle');
    if(b){
        divEdicio.style.visibility = "visible";
    }else{
        divEdicio.style.visibility = "collapse";
    }
}

function getAreaPoligons(){
    var area = 0;
    for(var i=0;i<vectors.features.length;i++){
        area += vectors.features[i].geometry.getArea();
    }
    return area;
}

/*
 * APIMethod: createGeodesicPolygon
 * Create a regular polygon around a radius. Useful for creating circles
 * and the like.
 *
 * Parameters:
 * origin - {<OpenLayers.Geometry.Point>} center of polygon. S'assumeix en lat/long
 * radius - {Float} distance to vertex, in map units.
 * sides - {Integer} Number of sides. 20 approximates a circle.
 * rotation - {Float} original angle of rotation, in degrees.
 * projection - {<OpenLayers.Projection>} the map's projection (EPSG:900913)
 */
function createGeodesicPolygon(origin, radius, sides, rotation, projection){
    var latlon = new OpenLayers.LonLat(origin.x, origin.y);

    var angle;
    var new_lonlat, geom_point;
    var points = [];

    for (var i = 0; i < sides; i++) {
        angle = (i * 360 / sides) + rotation;
        new_lonlat = OpenLayers.Util.destinationVincenty(latlon, angle, radius);
        new_lonlat.transform(new OpenLayers.Projection("EPSG:4326"), projection);
        geom_point = new OpenLayers.Geometry.Point(new_lonlat.lon, new_lonlat.lat);
        points.push(geom_point);
    }
    var ring = new OpenLayers.Geometry.LinearRing(points);
    return new OpenLayers.Geometry.Polygon([ring]);
}

function initArbre(info){
    if(info == null || info==false){
        $(function() {
            $( "#tabsctrlmapa" ).tabs({disabled: [2]});
        });
        $('#botoinfo').hide();
        if(map){
            map.removeControl(info_ctrl);
        }
    }else{
        $(function() {
            $( "#tabsctrlmapa" ).tabs();
        });
    }

    $(function() {
            $("#tree").jstree({
                "json_data" : jsonData
                ,"themes" : {"theme" : "classic"}
                ,"crrm" : {
			"move" : {
				"check_move" : function (m) {
					var p = this._get_parent(m.o);
					if(!p) return false;
					p = p == -1 ? this.get_container() : p;
					if(p === m.np) return true;
					if(p[0] && m.np[0] && p[0] === m.np[0]) return true;
					return false;
				}
			}
		},
		"dnd" : {
			"drop_target" : false,
			"drag_target" : false
		},
                "plugins" : [ "themes", "json_data", "checkbox", "ui","crrm","dnd" ]
            })
            .bind("loaded.jstree", function(event, data) {
                if(typeof configuraCarpetesICheckbox == 'function'){
                    configuraCarpetesICheckbox();
                }
                if(typeof seleccionaCapesVisibles == 'function'){
                    seleccionaCapesVisibles();
                }
                aplicaLlegendes();
                amagaDecoracionsLlegenda();
                aplicaKMLiGoogle();
                if(typeof amagaKMLiGoogle == 'function'){
                    amagaKMLiGoogle();
                }
                getCapesSeleccionades();
                getCapesDeSeleccionades();
            })
            .bind("before.jstree", function (e, data) {
                if(data.func == "uncheck_node"){
                    if(nodeEsFillDeBaseLayer(data.args[0]) && !permetUnCheck){
                        e.stopImmediatePropagation();
                        return false;
                    }else{
                        permetUnCheck = false;
                    }
                }
            })
            .bind("change_state.jstree", function (node, uncheck) {
                gestionaClicArbre(node, uncheck);
                getCapesSeleccionades();
                getCapesDeSeleccionades();
            })
            .delegate("a","click", function(e) {
                if(e.currentTarget.id && (e.currentTarget.id.substr(0,4)=='kml_' ||
                    e.currentTarget.id.substr(0,7)=='gearth_') ){
                    var open_link = window.open('','_blank');
                    open_link.location=e.target.parentNode.href;
                }
            })
    });
}

function amagaCheckBoxCarpeta(idselector){
    $('#'+idselector).find('ins.jstree-checkbox').each(
        function(index,element){
            if(element.parentNode.nodeName=="A" && index == 0 )
                $(element).hide();
        }
    );
}

function amagaIconaCarpeta(idselector){
    $('#'+idselector).find('ins.jstree-icon').each(
        function(index,element){
            if(element.parentNode.nodeName=="A")
                $(element).hide();
        }
    );
}

function amagaIconaCarpetaSegonNivellExcepte(array){
    var ulRoot = $('#tree > ul'); //ul descendent directe de #tree
    $( ulRoot ).find('> li').each( //li descedent directe de ul
        function(index,element){
            if(element.id){
                if(array.indexOf(element.id) < 0){
                    $( element ).find('ul li a ins.jstree-icon').hide();                    
                }
            }            
        }
    );
}

function amagaDecoracionsLlegenda(){
    $('li[id^="llegenda_"]').each(
        function(index,element){
            $(element).find('ins.jstree-icon').each(
                function(indexsub,elemsub){
                    $(elemsub).hide();
                }
            );
            $(element).find('ins.jstree-checkbox').each(
                function(indexsub,elemsub){
                    $(elemsub).hide();
                }
            );
        }
    );
}

function amagaCheckBoxPrimerNivellIconaSegonNivell(idselector){
    $('#' + idselector).find('ins.jstree-icon').each(
            function(index,element){
                if(element.parentNode.nodeName=="A" && index != 1)
                    $(element).hide();
            }
        );
    $('#' + idselector).find('ins.jstree-checkbox').each(
        function(index,element){
            if(element.parentNode.nodeName=="A" && index == 0)
                $(element).hide();
        }
    );
}

function nodeEsFillDeBaseLayer(node){
    if(node.parentNode == null)
        return false;
    else{
        if(node.parentNode.id=="baselayers"){
            return true;
        }else{
            return nodeEsFillDeBaseLayer(node.parentNode);
        }
    }
}

function getCapesSeleccionades(){
    $.jstree._reference("#tree").get_checked().find("li").andSelf().each(function(index,element){
        if(map){
            var layer = map.getLayersByName(element.id)[0];
            if(layer!=null){
                if(nodeEsFillDeBaseLayer(element)){
                    map.setBaseLayer(layer);
                    map.baseLayer.setVisibility(true);
                }else{
                    layer.setVisibility(true);
                }
            }
        }
    });
}

function seleccionaCapa(idCapa){
    $.jstree._reference("#tree").check_node('#'+idCapa);
}

function desplegaNode(idNode){
    $.jstree._reference("#tree").toggle_node('#'+idNode);
}

function getCapesDeSeleccionades(){
    $.jstree._reference("#tree").get_unchecked().find("li").andSelf().each(function(index,element){
        if(map){
            var layer = map.getLayersByName(element.id)[0];
            if(layer!=null && !nodeEsFillDeBaseLayer(element)){
                layer.setVisibility(false);
            }
        }
    });
}

function getIdElementPare(node){
    return node.parentNode.parentNode.id;
}

function gestionaClicArbre(node,uncheck){
    //Es un node de capa base
    if(getIdElementPare(uncheck.rslt[0]) == "baselayers"){
        if(!uncheck.args[1]){//Si hi havia algun altre node seleccionat, el deseleccionem
            var idNodeSelec = uncheck.rslt[0].id;
            var nodePare = uncheck.rslt[0].parentNode;
            for(var i = 0; i < nodePare.children.length; i++){
                if(nodePare.children[i] != null &&
                nodePare.children[i].id != "" &&
                nodePare.children[i].id != idNodeSelec){
                    if($.jstree._reference("#tree").is_checked(nodePare.children[i]))
                        permetUnCheck = true;
                        $.jstree._reference("#tree").uncheck_node(nodePare.children[i]);
                }
            }
        }
    }
}

function eliminaKMLiGoogle(idcapa){
    $('a[id="kml_' + idcapa + '"]').hide();
    $('a[id="gearth_' + idcapa + '"]').hide();
}

function eliminaKMLiGoogleTot(){
    $("'a[id*='kml_']").hide();
    $("'a[id*='gearth_']").hide();
}

function aplicaKMLiGoogle(){
    $('div.jstree').find('li').each(
        function(index,element){
            if(element.attributes['idlayergs']){
//                if(element.parentElement && element.parentElement.parentElement && element.parentElement.parentElement.id!="baselayers"){
                if(element.parentNode.parentNode.id!="baselayers"){
                    var capa = getCapaDeIdLlista(element.id);
                    var elem;
                    if( capa && capa.params && capa.params.CQL_FILTER){
                        elem = '<a id="kml_'+ element.id +'" href="http://'+urlServidor+'/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName='+element.attributes['idlayergs'].value+'&outputFormat=SHAPE-ZIP&CQL_FILTER=' + encodeURIComponent(capa.params.CQL_FILTER) + '" target="_blank"><img src="../grafics/page_shp12.png"></a>';
                        $(element).append(elem);
                        elem = '<a id="gearth_'+ element.id +'" href="http://'+urlServidor+'/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers='+element.attributes['idlayergs'].value+'&styles=&CQL_FILTER=' + encodeURIComponent(capa.params.CQL_FILTER) + '&bbox=246809.50679615702,4429945.3655678565,531814.7343779552,4804968.5619192235&width=389&height=512&srs=EPSG:23031&format=application/vnd.google-earth.kml+xml" target="_blank"><img src="../grafics/kml12.png"></a>';
                        $(element).append(elem);
                    }else{
                        elem = '<a id="kml_'+ element.id +'" href="http://'+urlServidor+'/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName='+element.attributes['idlayergs'].value+'&outputFormat=SHAPE-ZIP" target="_blank"><img src="../grafics/page_shp12.png"></a>';
                        $(element).append(elem);
                        elem = '<a id="gearth_'+ element.id +'" href="http://'+urlServidor+'/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers='+element.attributes['idlayergs'].value+'&styles=&bbox=246809.50679615702,4429945.3655678565,531814.7343779552,4804968.5619192235&width=389&height=512&srs=EPSG:23031&format=application/vnd.google-earth.kml+xml" target="_blank"><img src="../grafics/kml12.png"></a>';
                        $(element).append(elem);
                    }
                }
            }
        }
    );
}

function aplicaKMLiGoogleACapa(idCapa){
    $('div.jstree').find('li').each(
        function(index,element){
            if(element.attributes['idlayergs']){
                if(element.parentNode.parentNode.id!="baselayers"){
                    if(element.id==idCapa){
                        var capa = getCapaDeIdLlista(element.id);
                        var elem;
                        if(capa.params && capa.params.CQL_FILTER){
                            $('a[id="kml_' + idCapa + '"]').remove();
                            elem = '<a id="kml_'+ element.id +'" href="http://'+urlServidor+'/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName='+element.attributes['idlayergs'].value+'&outputFormat=SHAPE-ZIP&CQL_FILTER=' + encodeURIComponent(capa.params.CQL_FILTER) + '" target="_blank"><img src="../grafics/page_shp12.png"></a>';
                            $(element).append(elem);
                            $('a[id="gearth_' + idCapa + '"]').remove();
                            elem = '<a id="gearth_'+ element.id +'" href="http://'+urlServidor+'/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers='+element.attributes['idlayergs'].value+'&styles=&CQL_FILTER=' + encodeURIComponent(capa.params.CQL_FILTER) + '&bbox=246809.50679615702,4429945.3655678565,531814.7343779552,4804968.5619192235&width=389&height=512&srs=EPSG:23031&format=application/vnd.google-earth.kml+xml" target="_blank"><img src="../grafics/kml12.png"></a>';
                            $(element).append(elem);
                        }else{
                            $('a[id="kml_' + idCapa + '"]').remove();
                            elem = '<a id="kml_'+ element.id +'" href="http://'+urlServidor+'/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName='+element.attributes['idlayergs'].value+'&outputFormat=SHAPE-ZIP" target="_blank"><img src="../grafics/page_shp12.png"></a>';
                            $(element).append(elem);
                            $('a[id="gearth_' + idCapa + '"]').remove();
                            elem = '<a id="gearth_'+ element.id +'" href="http://'+urlServidor+'/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers='+element.attributes['idlayergs'].value+'&styles=&bbox=246809.50679615702,4429945.3655678565,531814.7343779552,4804968.5619192235&width=389&height=512&srs=EPSG:23031&format=application/vnd.google-earth.kml+xml" target="_blank"><img src="../grafics/kml12.png"></a>';
                            $(element).append(elem);
                        }
                    }
                }
            }
        }
    );
}

function aplicaLlegendes(){
    $('div.jstree').find('li').each(
        function(index,element){
            if(element.id.substring(0,9)=='llegenda_'){
                var img = '<div><img src="http://' + urlServidor + '/geoserver/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=5&HEIGHT=5&LAYER=' + element.parentNode.parentNode.attributes[1].nodeValue + '&LEGEND_OPTIONS=fontSize:9;dx:0;dy:0.2;mx:0;my:0.2"></div>'
                $(element).find("a").append('<ins style="height:auto;">'+ img +'</ins>');
                //$(element).find("a").append('<ins style="background-image:url(http://kilauea.creaf.uab.es/geoserver/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=5&HEIGHT=5&LAYER=' + element.id.substring(9) + '&LEGEND_OPTIONS=fontSize:8;dx:0;dy:0.2;mx:0;my:0.2);width:150px;height:75px;" ></ins>');
           }
        }
    );
}

function initLandMarkSearch(){
    $( "#landmark" ).autocomplete({
                            source: function( request, response ) {
                                    $.ajax({
                                            url: "http://ws.geonames.org/searchJSON",
                                            dataType: "jsonp",
                                            data: {
//                                                    featureClass: "P",
                                                    style: "full",
                                                    maxRows: 12,
                                                    name_startsWith: request.term,
                                                    username: 'exocat'
                                            },
                                            success: function( data ) {
                                                    response( $.map( data.geonames, function( item ) {

                                                            return {
                                                                    lat: item.lat,
                                                                    lng: item.lng,
                                                                    label: item.name + (item.adminName1 ? ", " + item.adminName1 : "") + ", " + item.countryName + " - " + item.lat+", "+ item.lng,
                                                                    value: item.name
                                                            }
                                                    }));


                                            }
                                    });
                            },
                            minLength: 2,
                            select: function( event, ui ) {
                                var proj = new OpenLayers.Projection("EPSG:4326");
                                var bounds = new OpenLayers.Bounds(ui.item.lng,ui.item.lat,ui.item.lng,ui.item.lat)
                                bounds.transform(proj, map.getProjectionObject());
                                map.zoomToExtent(bounds);
                            },
                            open: function() {
                                    $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
                            },
                            close: function() {
                                    $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
                            }
                    });
}