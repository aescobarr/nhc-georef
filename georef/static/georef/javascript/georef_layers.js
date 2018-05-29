$(document).ready(function() {

    var centroides_calc =  {
        name: 'centroides_calc_museu',
        layer : L.tileLayer.wms(
            'http://127.0.0.1:8080/geoserver/mzoologia/wms?',
            {
                layers: 'mzoologia:toponimsdarreraversio_nocalc',
                format: 'image/png',
                transparent: true
            }
        )
    };

    var centroides_digit =  {
        name: 'centroides_digit',
        layer : L.tileLayer.wms(
            'http://127.0.0.1:8080/geoserver/mzoologia/wms?',
            {
                layers: 'mzoologia:toponimsdarreraversio_radi',
                format: 'image/png',
                transparent: true,
                opacity: 0.4
            }
        )
    };

    var toponims =  {
        name: 'toponims',
        layer : L.tileLayer.wms(
            'http://127.0.0.1:8080/geoserver/mzoologia/wms?',
            {
                layers: 'mzoologia:toponimsdarreraversio',
                format: 'image/png',
                transparent: true,
                opacity: 0.4
            }
        )
    };

    var recursos_digit = {
        name: 'recursos_digit',
        layer : L.tileLayer.wms(
            'http://127.0.0.1:8080/geoserver/mzoologia/wms?',
            {
                layers: 'mzoologia:recursosgeoreferenciacio',
                format: 'image/png',
                transparent: true,
                opacity: 0.4
            }
        )
    }

    var recursos_wms = {
        name: 'recursos_wms',
        layer : L.tileLayer.wms(
            'http://127.0.0.1:8080/geoserver/mzoologia/wms?',
            {
                layers: 'mzoologia:recursosgeoreferenciacio_wms_bound',
                format: 'image/png',
                transparent: true,
                opacity: 0.4
            }
        )
    }

    var overlay_list = [];
    overlay_list.push(centroides_calc);
    overlay_list.push(centroides_digit);
    overlay_list.push(toponims);
    overlay_list.push(recursos_digit);
    overlay_list.push(recursos_wms);

    var overlays_control_config = [
        {
            groupName: 'Toponims',
            expanded: true,
            layers: {
                'Centroides de topònims calculats pel museu': centroides_calc.layer,
                'Centroides de topònims extrets de la digitalització': centroides_digit.layer,
                'Darreres versions de topònims': toponims.layer,
            }
        },
        {
            groupName: 'Recursos de georeferenciació',
            expanded: true,
            layers: {
                'Recursos de georeferenciació (límits digitalitzats)': recursos_digit.layer,
                'Recursos de georeferenciació (límits de les capes wms associades)': recursos_wms.layer,
            }
        }
    ];

    map_options = {
        editable:                   false,
        consultable:                true,
        overlays:                   overlay_list,
        overlays_control_config:    overlays_control_config,
        wms_url:                    wms_url
    };

    map_options.consultable = [
        centroides_calc.layer,
        centroides_digit.layer,
        toponims.layer,
        recursos_digit.layer,
        recursos_wms.layer
    ];

    var toponimsdarreraversio_nocalc_formatter = function(data){
        var html = '';
        html += '<style type="text/css">li.titol {font-size: 80%;padding:2px; } li.text {font-size: 100%;padding:2px;} a.linkFitxa{color:#00008B;text-align:right;padding:2px;} table.contingut{font-size: 80%;width:100%;} th, td {border: none;} td.atribut {text-align:right;vertical-align:top;padding:2px;} td.valor {text-align:left;padding:2px;} th.aladreta{text-align:right;padding:2px;} th.alesquerra{text-align:left;padding:2px;}</style>';
        html += '<table class="contingut"><tbody>';
        html += '<tr><th class="alesquerra">Centroides de topònims calculats pel museu</th>';
        html += '<tr><td class="atribut">Nom toponim : </td><td class="valor">' + data.properties.nomtoponim + '</td></tr>';
        html += '<tr><td class="atribut">Coord. x centroide : </td><td class="valor">' + data.properties.coordenada_x_centroide + '</td></tr>';
        html += '<tr><td class="atribut">Coord. y centroide : </td><td class="valor">' + data.properties.coordenada_y_centroide + '</td></tr>';
        html += '<tr><td class="atribut">Precisió centroide (m) : </td><td class="valor">' + data.properties.precisio_h + '</td></tr>';
        html += '</tbody></table></br>';
        return html;
    };

    var toponimsdarreraversio_radi_formatter = function(data){
        var html = '';
        html += '<style type="text/css">li.titol {font-size: 80%;padding:2px; } li.text {font-size: 100%;padding:2px;} a.linkFitxa{color:#00008B;text-align:right;padding:2px;} table.contingut{font-size: 80%;width:100%;} th, td {border: none;} td.atribut {text-align:right;vertical-align:top;padding:2px;} td.valor {text-align:left;padding:2px;} th.aladreta{text-align:right;padding:2px;} th.alesquerra{text-align:left;padding:2px;}</style>';
        html += '<table class="contingut"><tbody>';
        html += '<tr><th class="alesquerra">Centroides de topònims extrets de la digitalització</th>';
        html += '<tr><td class="atribut">Nom toponim : </td><td class="valor">' + data.properties.nomtoponim + '</td></tr>';
        html += '<tr><td class="atribut">Coord. x centroide : </td><td class="valor">' + data.properties.coordenada_x_centroide + '</td></tr>';
        html += '<tr><td class="atribut">Coord. y centroide : </td><td class="valor">' + data.properties.coordenada_y_centroide + '</td></tr>';
        html += '<tr><td class="atribut">Precisió centroide (m) : </td><td class="valor">' + data.properties.precisio_h + '</td></tr>';
        html += '</tbody></table></br>';
        return html;
    }

    var toponimsdarreraversio_formatter = function(data){
        var html = '';
        html += '<style type="text/css">li.titol {font-size: 80%;padding:2px; } li.text {font-size: 100%;padding:2px;} a.linkFitxa{color:#00008B;text-align:right;padding:2px;} table.contingut{font-size: 80%;width:100%;} th, td {border: none;} td.atribut {text-align:right;vertical-align:top;padding:2px;} td.valor {text-align:left;padding:2px;} th.aladreta{text-align:right;padding:2px;} th.alesquerra{text-align:left;padding:2px;}</style>';
        html += '<table class="contingut"><tbody>';
        html += '<tr><th class="alesquerra">Darreres versions de topònims</th>';
        html += '<tr><td class="atribut">Nom topònim : </td><td class="valor">' + data.properties.nomtoponim + '</td></tr>';
        html += '<tr><td class="atribut">Aquàtic? : </td><td class="valor">' + data.properties.aquatic + '</td></tr>';
        html += '<tr><td class="atribut">Tipus de topònim : </td><td class="valor">' + data.properties.tipustoponim + '</td></tr>';
        html += '<tr><td class="atribut">Número de versió : </td><td class="valor">' + data.properties.numero_versio + '</td></tr>';
        html += '</tbody></table></br>';
        return html;
    }

    var recursosgeoreferenciacio_formatter = function(data){
        var html = '';
        html += '<style type="text/css">li.titol {font-size: 80%;padding:2px; } li.text {font-size: 100%;padding:2px;} a.linkFitxa{color:#00008B;text-align:right;padding:2px;} table.contingut{font-size: 80%;width:100%;} th, td {border: none;} td.atribut {text-align:right;vertical-align:top;padding:2px;} td.valor {text-align:left;padding:2px;} th.aladreta{text-align:right;padding:2px;} th.alesquerra{text-align:left;padding:2px;}</style>';
        html += '<table class="contingut"><tbody>';
        html += '<tr><th class="alesquerra">Recursos de georeferenciació (límits digitalitzats)</th>';
        html += '<tr><td class="atribut">Nom recurs : </td><td class="valor">' + data.properties.nom + '</td></tr>';
        html += '<tr><td class="atribut">Acrònim : </td><td class="valor">' + data.properties.acronim + '</td></tr>';
        html += '</tbody></table></br>';
        return html;
    }

    var recursosgeoreferenciacio_wms_bound_formatter = function(data){
        var html = '';
        html += '<style type="text/css">li.titol {font-size: 80%;padding:2px; } li.text {font-size: 100%;padding:2px;} a.linkFitxa{color:#00008B;text-align:right;padding:2px;} table.contingut{font-size: 80%;width:100%;} th, td {border: none;} td.atribut {text-align:right;vertical-align:top;padding:2px;} td.valor {text-align:left;padding:2px;} th.aladreta{text-align:right;padding:2px;} th.alesquerra{text-align:left;padding:2px;}</style>';
        html += '<table class="contingut"><tbody>';
        html += '<tr><th class="alesquerra">Recursos de georeferenciació (límits de les capes wms associades)</th>';
        html += '<tr><td class="atribut">Nom recurs : </td><td class="valor">' + data.properties.nom + '</td></tr>';
        html += '<tr><td class="atribut">Acrònim : </td><td class="valor">' + data.properties.acronim + '</td></tr>';
        html += '</tbody></table></br>';
        return html;
    }

    map_options.formatters = {
        'toponimsdarreraversio_nocalc' : toponimsdarreraversio_nocalc_formatter,
        'toponimsdarreraversio_radi' : toponimsdarreraversio_radi_formatter,
        'toponimsdarreraversio' : toponimsdarreraversio_formatter,
        'recursosgeoreferenciacio' : recursosgeoreferenciacio_formatter,
        'recursosgeoreferenciacio_wms_bound' : recursosgeoreferenciacio_wms_bound_formatter
    };

    map = new djangoRef.Map.createMap(map_options);

});