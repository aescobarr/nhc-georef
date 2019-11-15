$(document).ready(function() {
    table = $('#users_list').DataTable( {
        'ajax': {
            'url': _user_list_url,
            'dataType': 'json'
        },
        'serverSide': true,
        'processing': true,
        "language": opcions_llenguatge,
        'pageLength': 25,
        'pagingType': 'full_numbers',
        'bLengthChange': false,
        stateSave: true,
        //"dom": '<"toolbar"><"top"iflp<"clear">>rt<"bottom"iflp<"clear">>',
        'dom': '<"top"iflp<"clear">>rt<"bottom"iflp<"clear">>',
        stateSaveCallback: function(settings,data) {
            localStorage.setItem( 'DataTables_' + settings.sInstance, JSON.stringify(data) );
        },
        stateLoadCallback: function(settings) {
            return JSON.parse( localStorage.getItem( 'DataTables_' + settings.sInstance ) );
        },
        'columns': [
            { 'data': 'user.username' }
            ,{ 'data': 'user.first_name' }
            ,{ 'data': 'user.last_name' }
            ,{ 'data': 'user.email' }
            ,{ 'data': 'organization.name' }
        ],
        'columnDefs': [
            {
                'targets':0,
                'title': gettext('Usuari')
            },
            {
                'targets':1,
                'title': gettext('Nom')
            },
            {
                'targets':2,
                'title': gettext('1er cognom')
            },
            {
                'targets':3,
                'title': gettext('Correu-e')
            },
            {
                'targets':4,
                'title': gettext('Organització')
            },
            {
                'targets': 5,
                'data': null,
                'sortable': false,
                'defaultContent': '<button title="' + gettext('Esborrar usuari') + '" class="delete_button btn btn-danger"><i class="fa fa-times" aria-hidden="true"></i></button>'
            },
            {
                'targets': 6,
                'data': null,
                'sortable': false,
                'defaultContent': '<button title="' + gettext('Editar perfil') + '" class="edit_button btn btn-info"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>'
            },
            {
                'targets': 7,
                'data': null,
                'sortable': false,
                'defaultContent': '<button title="' + gettext('Canviar password') + '" class="chgpsswd_button btn btn-danger"><i class="fa fa-lock"></i></button>'
            }
        ]
    } );

    var delete_usuari = function(id){
        $.ajax({
            url: _user_delete_url + id,
            method: 'DELETE',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                toastr.success(gettext('Usuari esborrat amb èxit!'));
                table.ajax.reload();
            },
            error: function(jqXHR, textStatus, errorThrown){
                toastr.error(gettext('Error esborrant'));
            }
        });
    };

    var confirmDialog = function(message,id){
        $('<div></div>').appendTo('body')
            .html('<div><h6>'+message+'</h6></div>')
            .dialog({
                modal: true, title: gettext('Esborrant usuari...'), zIndex: 10000, autoOpen: true,
                width: 'auto', resizable: false,
                buttons: {
                    Yes: function () {
                        delete_usuari(id);
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

    $( '#addUser' ).click(function() {
        var url = _add_user_url;
        window.location.href = url;
    });

    $('#users_list tbody').on('click', 'td button.edit_button', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        var id = row.data().user.id;
        url = '/user/profile/' + id + '/';
        window.location.href = url;
    });

    $('#users_list tbody').on('click', 'td button.chgpsswd_button', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        var id = row.data().user.id;
        url = '/user/password/change/' + id;
        window.location.href = url;
    });

    $('#users_list tbody').on('click', 'td button.delete_button', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        var id = row.data().user.id;
        confirmDialog(gettext("S'esborrarà l'usuari '") + row.data().user.first_name + " " + row.data().user.last_name + gettext("'! Segur que vols continuar?"),id);
    });
});