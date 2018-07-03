(function(){

    if (typeof(jQuery.fn.DataTable) == 'undefined') throw 'DataTables must be loaded';

    if (typeof djangoRef === 'undefined') this.djangoRef = {};

    if (typeof djangoRef.GenericThesaurus === 'undefined') this.djangoRef.GenericThesaurus = {};

    djangoRef.GenericThesaurus.table = null;

    djangoRef.GenericThesaurus.create = function(options){
        options = options || {};
        options = $.extend({},
        {
            column_name: 'Nom'
        },
        options);

        if (options.data_url == null) throw 'Missing mandatory parameter data_url';

        if (options.crud_url == null) throw 'Missing mandatory parameter crud_url';

        djangoRef.GenericThesaurus.table = $('#element_list').DataTable( {
            'ajax': {
                'url': options.data_url,
                'dataType': 'json'
            },
            'serverSide': true,
            'processing': true,
            "language": opcions_llenguatge_catala,
            'pageLength': 25,
            'pagingType': 'full_numbers',
            'bLengthChange': false,
            stateSave: true,
            'dom': '<"top"iflp<"clear">>rt<"bottom"iflp<"clear">>',
            stateSaveCallback: function(settings,data) {
                localStorage.setItem( 'DataTables_' + settings.sInstance, JSON.stringify(data) );
            },
            stateLoadCallback: function(settings) {
                return JSON.parse( localStorage.getItem( 'DataTables_' + settings.sInstance ) );
            },
            'columns': [
                { 'data': options.text_field_name }
            ],
            'columnDefs': [
                {
                    'targets': 1,
                    'data': 'editable',
                    'sortable': false,
                    'defaultContent': '<button class="delete_button btn btn-danger"><i class="fa fa-times" aria-hidden="true"></i></button>'
                },
                {
                    'targets': 2,
                    'data': 'editable',
                    'sortable': false,
                    'defaultContent': '<button class="edit_button btn btn-info"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>'
                },
                {
                    'targets':0,
                    'title': options.column_name
                }
            ]
        } );

        var do_update = function(){
            _update($('#name_update').val(),$('#id').val());
        }

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

        var form_update = dialog_update.find( "form" ).on( "submit", function( event ) {
            event.preventDefault();
        });


        //return djangoRef.GenericThesaurus.table;
        var _update = function(new_nom, id){
            $.ajax({
                url: options.crud_url + encodeURI(id) + '/',
                data: JSON.parse("{ \"" + options.text_field_name + "\":\"" + new_nom + "\"}"),
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
                    djangoRef.GenericThesaurus.table.ajax.reload();
                },
                error: function(jqXHR, textStatus, errorThrown){
                    toastr.error('Error actualitzant!');
                }
            });
        }

        var do_add = function(){
            _add($('#name').val());
        };

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

        var form_create = dialog_create.find( "form" ).on( "submit", function( event ) {
            event.preventDefault();
        });

        var _add = function(nom){
            $.ajax({
                url: options.crud_url,
                data: JSON.parse("{ \"" + options.text_field_name + "\":\"" + nom + "\"}"),
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
                    djangoRef.GenericThesaurus.table.ajax.reload();
                },
                error: function(jqXHR, textStatus, errorThrown){
                    toastr.error('Error afegint!');
                }
            });
        }

        var _delete = function(id){
            $.ajax({
                url: options.crud_url + encodeURI(id) + '/',
                method: 'DELETE',
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        var csrftoken = getCookie('csrftoken');
                        xhr.setRequestHeader('X-CSRFToken', csrftoken);
                    }
                },
                success: function( data, textStatus, jqXHR ) {
                    toastr.success('Esborrat amb èxit!');
                    djangoRef.GenericThesaurus.table.ajax.reload();
                },
                error: function(jqXHR, textStatus, errorThrown){
                    toastr.error('Error esborrant!');
                }
            });
        };

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

        $( "#add" ).button().on( "click", function() {
            dialog_create.dialog( "open" );
        });

        $('#element_list tbody').on('click', 'td button.edit_button', function () {
            var tr = $(this).closest('tr');
            var row = djangoRef.GenericThesaurus.table.row( tr );
            var id = row.data().id;
            var name = row.data()[options.text_field_name];
            $('#id').val(id);
            $('#name_update').val(name);
            dialog_update.dialog( "open" );
        });

        $('#element_list tbody').on('click', 'td button.delete_button', function () {
            var tr = $(this).closest('tr');
            var row = djangoRef.GenericThesaurus.table.row( tr );
            var id = row.data().id;
            confirmDialog("S'esborrarà '" + row.data()[options.text_field_name] + "'! Segur que vols continuar?",id);
        });

    }

})();
