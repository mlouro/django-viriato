$(document).ready(function(){
    $("#table_details tr:last td:eq(1) input").change(function(){
        if ($("#table_details tr:last td:eq(1) input").val()!=""){
            add_new_row("table_details");
            add_add_row_event('table_details');
            copy_tax_and_retention_values("table_details");
            rename_hide_button("table_details");
            add_calculate_totals_event('table_details');
        }
    });

    $('#dialog').jqm({
        modal: true,
        trigger: 'a#importMilestones',
        overlay: 88,
        onHide: function(h) {
            h.w.fadeOut(888); // hide window
            h.o.remove(); // remove overlay
        },
    });

    $('#dialog').jqmAddClose('#import_button');

    $('a#importMilestones').click(function(){
        get_companys();
    });

    $('#id_con-date').datepicker();

    add_calculate_totals_event('table_details');


});

function totals(){
    $('#id_con-total_impact_value').val(calculate_totals('table_details', 2, 3));
        $('#id_con-total_tax_value').val(calculate_others('table_details', 2, 3, 4));
        $('#id_con-total_retention_value').val(calculate_others('table_details', 2, 3, 5));
        $('#id_con-total').val(
            parseFloat($('#id_con-total_impact_value').val()) +
            parseFloat($('#id_con-total_tax_value').val()) -
            parseFloat($('#id_con-total_retention_value').val())
        );
}





function add_calculate_totals_event(table){
    table = '#' + table;
    $(table + ' tr:last td:eq(2) input').blur(function(){
        totals();
    });

    $(table + ' tr:last td:eq(3) input').blur(function(){
        totals();
    });

    $(table + ' tr:last td:eq(4) input').blur(function(){
        totals();
    });

    $(table + ' tr:last td:eq(5) input').blur(function(){
        totals();
    });
}

function get_companys(){
    $.post("/invoice/company/company_ajax/",
        {},
        function(data){
            select_box = '<select id="company_select_box">';
            for (i in data)
                select_box += '<option value="' + data[i].pk + '">' + data[i].fields.title + ' - ' + data[i].fields.legal_name +'</option>';
            select_box += '</select>';
            $("#companyAjax").html(select_box);
            add_ajax_event_to_company();
            get_projects($('#company_select_box').val());
        },
        "json"
    );

}

function get_projects(company_id){
    $.post("/invoice/contract/project_ajax/",
        { company_id : company_id },
        function(data){
            select_box = '<select id="project_select_box">';
            for (i in data)
                select_box += '<option value="' + data[i].pk + '">' + data[i].fields.name +'</option>';
            select_box += '</select>';
            $("#projectAjax").html(select_box);
            add_ajax_event_to_project();
            get_milestones($('#project_select_box').val());
        },
        "json"
    );
}

function add_ajax_event_to_company(){
    $('#company_select_box').change(function(){
        get_projects($('#company_select_box').val());
    });
}

function add_ajax_event_to_project(){
    $('#project_select_box').change(function(){
        get_milestones($('#project_select_box').val());
    });
}

function get_milestones(project_id){
    $.post("/invoice/contract/milestone_ajax/",
        { project_id : project_id },
        function(data){
            result =
                '<table class="stripes" id="milestones_table">' +
                    '<tr>' +
                        '<th class="select headers"> Select </th>' +
                        '<th class="title headers"> Milestone </th>' +
                    '</tr>'
            ;
            for (i in data)
                result +=
                    '<tr>' +
                        '<td class="select"><input type="checkbox" id="milestone_' + i + '"/></td >' +
                        '<td id="title_' + i + '">' + data[i].fields.title + '</td>' +
                    '</tr>'
            result += '</table>';
            $("#milestones").html(result);

            $(".stripes tr:even").addClass("alt");

            add_mouse_over_event();
        },
        "json"
    );
}


function import_milestones(){
    nr_rows = $("#milestones_table tr").length-1;
    o = document.getElementById("milestones_table");
    first_row = parseInt($('#id_details-INITIAL_FORMS').val()+1);

    for (i=0;i<nr_rows;i++){
        if (o.rows[i+1].cells[0].firstChild.checked)
            do_import((o.rows[i+1].cells[0].firstChild.id).split('_')[1]);
    }
    add_mouse_over_event();
    $(".stripes tr:even").addClass("alt");
    $("#id_con-company").val($("#company_select_box").val());
    $("#id_con-project").val($("#project_select_box").val());
}

function do_import(id){
    table = 'table_details';
    len = $('#table_details tr').length-1;
    $('#table_details tr:eq(' + len + ') td:eq(1) input').val($('#title_' + id).html());
    add_new_row('table_details');
    add_add_row_event('table_details');
    copy_tax_and_retention_values(table);
    rename_hide_button(table);
    add_calculate_totals_event(table);
}

function calculate_totals(table, col1, col2){
    table = '#' + table;
    nr_rows = $(table + ' tr').length;
    total = 0;

    for (i=1; i<nr_rows; i++){
        val_col1 = $(table + ' tr:eq(' + i + ') td:eq(' + col1 +') input').val();
        val_col2 = $(table + ' tr:eq(' + i + ') td:eq(' + col2 +') input').val();
        if (val_col1!=0 && val_col2 !=0)
            total +=  val_col1 * val_col2;
    }
    return total;
}

function calculate_others(table, col1, col2, other){
    table = '#' + table;
    nr_rows = $(table + ' tr').length;
    total = 0;

    for (i=1; i<nr_rows; i++){
        val_col1 = $(table + ' tr:eq(' + i + ') td:eq(' + col1 +') input').val();
        val_col2 = $(table + ' tr:eq(' + i + ') td:eq(' + col2 +') input').val();
        val_other = parseFloat($(table + ' tr:eq(' + i + ') td:eq(' + other +') input').val()) / 100;
        if (val_col1!=0 && val_col2 !=0)
            total +=  val_col1 * val_col2 * val_other;
    }
    return roundNumber(total, 2);
}
