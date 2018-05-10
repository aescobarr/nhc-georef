$(document).ready(function() {

    var table_options = {
        div_id : 'autors_list',
        column_name : 'Nom autor',
        data_url : _list_url
    };

    var dataTable = djangoRef.DataTableThesaurus.create(table_options);

    var _update = function(new_nom, id){
        $.ajax({
            url: _update_url + id,
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
                dialog.dialog('close');
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
                dialog.dialog('close');
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

    var _delete = function(id){
        $.ajax({
            url: _delete_url + id,
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

    var dialog = $( "#dialog-form" ).dialog({
      autoOpen: false,
      height: 300,
      width: 400,
      modal: true,
      buttons: {
        "Afegir Autor": do_add,
        Cancel: function() {
          dialog.dialog( "close" );
        }
      },
      close: function() {
        form[ 0 ].reset();
      }
    });

    $( "#add" ).button().on( "click", function() {
      dialog.dialog( "open" );
    });

    var form = dialog.find( "form" ).on( "submit", function( event ) {
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
        console.log(id);
    });

    $('#autors_list tbody').on('click', 'td button.delete_button', function () {
        var tr = $(this).closest('tr');
        var row = dataTable.row( tr );
        var id = row.data().id;
        confirmDialog("S'esborrarà '" + row.data().nom + "'! Segur que vols continuar?",id);
    });


});