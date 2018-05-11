$(document).ready(function() {

    var options = {
        div_id : 'autors_list',
        column_name : 'Nom autor',
        data_url : _list_url,
        update_url: _update_url
    };

    var dataTable = djangoRef.GenericThesaurus.create(options);

    var _update = function(new_nom, id){
        $.ajax({
            url: _update_url + encodeURI(id) + '/',
            data: { 'nom' : new_nom },
            method: 'PUT',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                toastr.success('Actualitzat amb èxit!');
                dialog_update.dialog('close');
                dataTable.ajax.reload();
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error('Error actualitzant!');
            }
        });
    }

    var _add = function(nom){
        $.ajax({
            url: _create_url,
            data: { 'nom' : nom },
            method: 'POST',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                toastr.success('Afegit amb èxit!');
                dialog_create.dialog('close');
                dataTable.ajax.reload();
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error('Error afegint!');
            }
        });
    }

    var do_add = function(){
        _add($('#name').val());
    }

    var do_update = function(){
        _update($('#name_update').val(),$('#id').val());
    }

    var _delete = function(id){
        $.ajax({
            url: _delete_url + encodeURI(id) + '/',
            method: 'DELETE',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                toastr.success('Esborrat amb èxit!');
                dataTable.ajax.reload();
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error('Error esborrant!');
            }
        });
    };

    var dialog_update = $( "#dialog-form-update" ).dialog({
        autoOpen: false,
        height: 300,
        width: 400,
        modal: true,
        buttons: {
            "Actualitzar": do_update,
            Cancel: function() {
                dialog_update.dialog( "close" );
            }
        },
        close: function() {
            form_update[ 0 ].reset();
        }
    });

    var dialog_create = $( "#dialog-form-create" ).dialog({
        autoOpen: false,
        height: 300,
        width: 400,
        modal: true,
        buttons: {
            "Crear": do_add,
            Cancel: function() {
                dialog_create.dialog( "close" );
            }
        },
        close: function() {
            form_create[ 0 ].reset();
        }
    });

    $( "#add" ).button().on( "click", function() {
        dialog_create.dialog( "open" );
    });

    var form_create = dialog_create.find( "form" ).on( "submit", function( event ) {
        event.preventDefault();
    });

    var form_update = dialog_update.find( "form" ).on( "submit", function( event ) {
        event.preventDefault();
    });

    var confirmDialog = function(message,id){
        $('<div></div>').appendTo('body')
            .html('<div><h6>'+message+'</h6></div>')
            .dialog({
                modal: true, title: 'Esborrant...', zIndex: 10000, autoOpen: true,
                width: 'auto', resizable: false,
                buttons: {
                    Yes: function () {
                        _delete(id);
                        $(this).dialog("close");
                    },
                    No: function () {
                        $(this).dialog("close");
                    }
                },
                close: function (event, ui) {
                    $(this).remove();
                }
        });
    };

    $('#autors_list tbody').on('click', 'td button.edit_button', function () {
        var tr = $(this).closest('tr');
        var row = dataTable.row( tr );
        var id = row.data().id;
        var name = row.data().nom;
        $('#id').val(id);
        $('#name_update').val(name);
        dialog_update.dialog( "open" );
    });

    $('#autors_list tbody').on('click', 'td button.delete_button', function () {
        var tr = $(this).closest('tr');
        var row = dataTable.row( tr );
        var id = row.data().id;
        confirmDialog("S'esborrarà '" + row.data().nom + "'! Segur que vols continuar?",id);
    });


});