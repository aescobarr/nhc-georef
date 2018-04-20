$(document).ready(function() {

    var show_data = function(centroid_x,centroid_y,unc){
        $('#val_x').text(centroid_x);
        $('#val_x').toggle( "highlight" );
        $('#val_y').text(centroid_y);
        $('#val_y').toggle( "highlight" );
        $('#val_inc').text(unc);
        $('#val_inc').toggle( "highlight" );
    }

    $( '#clipboard' ).click(function() {
        var text = '';
        text = 'lat:' + $('#val_y').text() + ' long:' + $('#val_x').text() + ' prec:' + $('#val_inc').text();
        copyToClipboard(text);
        toastr.success("Resultats copiats al portapapers!");
    });

    var computeCentroid = function(filename){
        show_data('','','');
        $.ajax({
            url: _compute_centroid_url + encodeURI(filename),
            method: "POST",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                 console.log(data);
                 show_data(data.detail.centroid_x, data.detail.centroid_y, data.detail.inc);
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error("Error calculant centroide - " + jqXHR.responseJSON.detail);
                console.log(jqXHR);
            }
        });
    }

    var uploader = new qq.FileUploader({
        action: _ajax_upload_url,
        element: $('#fileuploader')[0],
        multiple: false,
        onSubmit: function(id, fileName){
            $('#filename').val('');
            this.params.deletePrevious = true;
        },
        onComplete: function(id, fileName, responseJSON) {
            if(responseJSON.success) {
                //$('#filename').val(responseJSON.filename);
                //toastr.success('Fitxer carregat al servidor amb èxit!')
                computeCentroid(responseJSON.filename);
            } else {
                toastr.error('Error pujant fitxer!')
            }
        },
        template:'<div class="qq-uploader">' +
            '<div class="qq-upload-drop-area"><span>Importar shapefile (zip)</span></div>' +
            '<div class="qq-upload-button ui-widget-content ui-button ui-corner-all ui-state-default">Importar shapefile (zip)</div>' +
            '<ul class="qq-upload-list"></ul>' +
            '</div>',
        params: {
            'csrf_token': csrf_token,
            'csrf_name': 'csrfmiddlewaretoken',
            'csrf_xname': 'X-CSRFToken',
        }
    });

});