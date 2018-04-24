$(document).ready(function() {

    var import_csv = function(file){
        $.ajax({
            url: _import_csv_url + encodeURI(file),
            method: 'POST',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                //toastr.success('Capa WMS creada amb èxit!');
                //table.ajax.reload();
                //$('#id_nomcapa').val('');
                console.log(data.detail);
                $('.qq-upload-list').empty();
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(jqXHR.responseJSON);
                toastr.error(jqXHR.responseJSON.detail);
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
                toastr.success('Fitxer carregat al servidor amb èxit!')
                console.log(responseJSON.detail);
                import_csv(responseJSON.filename);
            } else {
                toastr.error('Error pujant fitxer!')
            }
        },
        template:'<div class="qq-uploader">' +
            '<div class="qq-upload-drop-area"><span>Pujar fitxer CSV</span></div>' +
            '<div class="qq-upload-button ui-widget-content ui-button ui-corner-all ui-state-default">Pujar fitxer CSV</div>' +
            '<ul class="qq-upload-list"></ul>' +
            '</div>',
        params: {
            'csrf_token': csrf_token,
            'csrf_name': 'csrfmiddlewaretoken',
            'csrf_xname': 'X-CSRFToken',
        }
    });

    $('#details').click(function(){
        //$('.persiana').toggle();
        if( $('.persiana').attr("style") == 'display: none;' ){
            $('.persiana').fadeIn( "slow", function(){});
        }else{
            $('.persiana').fadeOut( "slow", function(){});
        }
    });


});