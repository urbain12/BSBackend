
// Tables-DataTables.js
// ====================================================================

$(window).on('load', function() {


    // DATA TABLES
    // =================================================================
    // Require Data Tables
    // -----------------------------------------------------------------
    // http://www.datatables.net/
    // =================================================================
    $.fn.DataTable.ext.pager.numbers_length = 5;

    // Basic Data Tables with responsive plugin
    // -----------------------------------------------------------------

    var userLang = navigator.language || navigator.userLanguage;
    var urlLang = '';
    console.log('UserLanguage: ' + userLang);

    if (userLang == 'ja' || userLang == 'jp') {
        urlLang = "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Japanese.json";
    }
    $('#custom-dt-basic').dataTable( {
        "responsive": true,
        "language": {
            "url": urlLang,
            "paginate": {
              "previous": '<i class="demo-psi-arrow-left"></i>',
              "next": '<i class="demo-psi-arrow-right"></i>'
            }
        }
    } );

    /*
    console.log('Firing DataTables responsive plugin ...');
    var $table = $('#updatable-table');
    var $updatable = $('#updatable-row');
    $table.on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table', function () {
        $updatable.prop('disabled', !$table.bootstrapTable('getSelections').length);
    });

    $updatable.click(function () {
        console.log('checkbox clicked');

        var ids = $.map($table.bootstrapTable('getSelections'), function (row) {
            console.log('row.id = ' + row.id);
            return row.id
        });
        $table.bootstrapTable('remove', {
            field: 'id',
            values: ids
        });
        $updatable.prop('disabled', true);
    });
    */
});
