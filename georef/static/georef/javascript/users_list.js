$(document).ready(function() {
    table = $('#users_list').DataTable( {
        'ajax': {
            'url': _user_list_url,
            'dataType': 'json'
        },
        'serverSide': true,
        'processing': true,
        //"language": opcions_llenguatge_catala,
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
        ],
        'columnDefs': [
            {
                'targets':0,
                'title': 'Usuari'
            },
            {
                'targets':1,
                'title': 'Nom'
            },
            {
                'targets':2,
                'title': '1er cognom'
            },
            {
                'targets':3,
                'title': 'Correu-e'
            },
            {
                'targets': 4,
                'data': null,
                'sortable': false,
                'defaultContent': '<button class="delete_button btn btn-danger"><i class="fa fa-times" aria-hidden="true"></i></button>'
            },
            {
                'targets': 5,
                'data': null,
                'sortable': false,
                'defaultContent': '<button class="edit_button btn btn-info"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>'
            }
        ]
    } );

    $( '#addUser' ).click(function() {
        var url = _add_user_url;
        window.location.href = url;
    });
});