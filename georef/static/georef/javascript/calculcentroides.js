$(document).ready(function() {
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
                $('#filename').val(responseJSON.filename);
                toastr.success('Fitxer carregat al servidor amb èxit!')
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