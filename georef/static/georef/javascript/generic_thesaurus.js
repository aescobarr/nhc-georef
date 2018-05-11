(function(){

    if (typeof(jQuery.fn.DataTable) == 'undefined') throw 'DataTables must be loaded';

    if (typeof djangoRef === 'undefined') this.djangoRef = {};

    if (typeof djangoRef.GenericThesaurus === 'undefined') this.djangoRef.GenericThesaurus = {};

    djangoRef.GenericThesaurus.table = null;

    djangoRef.GenericThesaurus.create = function(options){
        options = options || {};
        options = $.extend({},
        {
            div_id: 'table',
            column_name: 'Nom'
        },
        options);

        if (options.data_url == null) throw 'Missing mandatory parameter data_url';

        if (options.update_url == null) throw 'Missing mandatory parameter update_url';

        djangoRef.GenericThesaurus.table = $('#' + options.div_id).DataTable( {
            'ajax': {
                'url': options.data_url,
                'dataType': 'json'
            },
            'serverSide': true,
            'processing': true,
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
                { 'data': 'nom' }
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

        return djangoRef.GenericThesaurus.table;
    }

})();
