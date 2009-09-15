var tax, retention;

$(document).ready(function(){
    tax = $("#tax").val();
    retention = $("#retention").val();

    $('#contractsAjax').change(function(){
        get_contracts_details($(this).val());
    });

//     $('#contracts_table').hide();
});

function set_with_project_functions(){
    add_focus_event(true);
    lock_fields();
    create_select_new_item();
}

function set_without_project_functions(){
    add_new_row('table_details');
    add_add_row_event('table_details', true);
    add_calculate_row_total_event();
    $('#table_details tr td:eq(5) INPUT[type="text"]').attr('readonly', true);
    $('.to_pay input').attr('readonly', true);
}

function add_calculate_row_total_event(){
    $("#table_details tr:last td:eq(2) input").change(function(){
        calculate_row_total($(this).attr('id'));
    });

    $("#table_details tr:last td:eq(3) input").change(function(){
        calculate_row_total($(this).attr('id'));
    });
}

function calculate_row_total(id){
    id_number = id.split('-')[1];
    uc = parseFloat($('#id_details-' + id_number + '-unity_cost').val());
    qt = parseFloat($('#id_details-' + id_number + '-quantity').val());
    tx = parseFloat($('#id_details-' + id_number + '-tax').val());
    ret = parseFloat($('#id_details-' + id_number + '-retention').val());
    isNaN(uc) ? uc = 0 : uc = uc;
    isNaN(qt) ? qt = 0 : qt = qt;
    isNaN(tx) ? tx = 0 : tx = tx;
    isNaN(ret) ? ret = 0 : ret = ret;
    imp = uc*qt;
    $('#id_details-' + id_number + '-total').val(roundNumber((imp) - (imp*tx) - (imp*ret),2));

    if (isNaN(parseInt($('#id_con-contract').val())))
        $('#id_details-' + id_number + '-to_pay').val(roundNumber((imp) - (imp*tx) - (imp*ret),2));
}

function add_calculate_totals_event(table){
    table = '#' + table;
    $(table + ' tr:last td:eq(2) input').blur(function(){
        calculate_totals();
    });

    $(table + ' tr:last td:eq(3) input').blur(function(){
        calculate_totals();
    });

    $(table + ' tr:last td:eq(4) input').blur(function(){
        calculate_totals();
    });

    $(table + ' tr:last td:eq(5) input').blur(function(){
        calculate_totals();
    });
}

function add_focus_event(contract){
    $('.to_pay input')
        .unbind()
        .focus(function(){
            pos = $(this).position();
            id_number = $(this).attr('id').split('-')[1];
            show_tip (pos.left, pos.top, $(this).width(), id_number, contract);
        })
        .blur(function(){
            $('#tooltip').hide();
            if (parseFloat($(this).val())>max_to_pay(id_number, contract))
                $(this).val(max_to_pay(id_number, contract));
            calculate_totals();
        })
    ;
}

function calculate_totals(){
    nr_cols = $('#table_details tr').length-1;
    ret = 0;
    tx = 0;
    imp = 0;
    for (i=1;i<=nr_cols;i++){
        cur_ret = parseFloat($('#table_details tr:eq(' + i + ') td:eq(9) input').val()) / 100;
        cur_tx = parseFloat($('#table_details tr:eq(' + i + ') td:eq(8) input').val()) / 100;
        cur_imp = parseFloat($('#table_details tr:eq(' + i + ') td:eq(5) input').val());

        !isNaN(cur_ret) && !isNaN(cur_imp) ? ret += cur_ret * cur_imp : ret += 0;
        !isNaN(cur_tx) && !isNaN(cur_imp) ? tx += cur_tx * cur_imp : tx += 0;
        !isNaN(cur_imp) ? imp += cur_imp : imp += 0;
    }
    $('#id_con-total_impact_value').val(roundNumber(imp,2));
    $('#id_con-total_tax_value').val(roundNumber(tx,2));
    $('#id_con-total_retention_value').val(roundNumber(ret,2));
    $('#id_con-total').val(roundNumber(imp - tx - ret,2));
}

function max_to_pay(id_number, contract){
    total = parseFloat($('#id_details-' + id_number + '-total').val());
    if (contract)
        isNaN(parseFloat($('#id_details-' + id_number + '-total_payed').val())) ? total_payed = 0 : total_payed = parseFloat($('#id_details-' + id_number + '-total_payed').val());
    else
        total_payed = 0;
    return roundNumber(total-total_payed,2);
}

function show_tip(x, y, w, id_number, contract){
    $('#tooltip')
        .css({
            'left' : x + w + 5,
            'top' : y
        })
        .fadeIn('slow')
        .html('Max: ' + max_to_pay(id_number, contract))
    ;
}

function have_contract(){
    create_new_dialog();
    get_contracts();
    $('#jqmOk').click(function(){
            if ($('#contracts_table .select INPUT[type="checkbox"]:checked').length>0){
                add_focus_event(true);
                import_to_receipt();
                set_with_project_functions();
            }
            else
                set_without_project_functions();
    });

    $('#jqmClose').click(function(){
        set_without_project_functions();
    });
    add_mouse_over_event();
}

function create_new_dialog(){
    $('#have_contract')
        .height(500)
        .width(800)
        .css({
            'margin-left' : '-400px',
            'top' : '5%',
            'left' : '50%',
        })
    ;

    $('#have_contract #content').css({
        'text-align' : 'left',
    });

    $('#have_contract #content').html($('#contracts').html());

    add_close_event_to_buttons();
}

function get_contracts(){
    $.post("/invoices/contract/contracts_ajax/",
        {},
        function(data){
            result = '';
//             result += '<option value="2"> sdsadsadsa </option>';
            for (i in data){
                result += '<option value="' + data[i].pk + '"> ' + data[i].fields.description + '</option>';
            }
            $('#contractsAjax')
                .html(result)
                .change(function(){get_contracts_details($(this).val())
            ;
    });
        },
        "json"
    );
    get_contracts_details(-1);
}

function get_contracts_details(contract_id){
    $('#contracts_table').show();
    $('#contracts_table tr:gt(1)').remove();
    $.post("/invoices/contract/contract_details_ajax/",
        {contract_id : contract_id},
        function(data){
            for (i in data){
                $('#contracts_table tr:last td:eq(0) input').attr('id','select_'+i);
                $('#contracts_table tr:last td:eq(1)')
                    .attr('id','title_'+i)
                    .html(data[i].fields.description);
                 $('#contracts_table tr:last td:eq(2) input')
                    .attr('id','pk_' + i)
                    .val(data[i].pk);
                $('#contracts_table tr:last td:eq(3) input')
                    .attr('id','total_payed_' + i)
                    .val(data[i].fields.total_payed);
                if (i<data.length-1)
                    $('#contracts_table').append($('#contracts_table tr:last').clone());
            }
            add_mouse_over_event();
            $(".stripes tr:even").addClass("alt");
            $('#contracts_table .title').click(function(){
                $('#select_'+$(this).attr("id").split('_')[1]).attr('checked', true);
            });
        },
        "json"
    );
}

function select_all(){
    if ($('#select_all').attr('checked'))
        $('#contracts_table INPUT[type="checkbox"]').attr('checked', true)
    else
        $('#contracts_table INPUT[type="checkbox"]').attr('checked', false)
}

function import_to_receipt(){
    $('#id_con-contract').val($('#contractsAjax').val());
    get_contract_inf($('#contractsAjax').val());
    table_nr_rows = $('#contracts_table tr').length-1;
    how_many_selected = $('#contracts_table .select INPUT[type="checkbox"]:checked').length;
    selected_items = '';
    for (i=0;i<table_nr_rows;i++){
        if ($('#contracts_table #select_' + i).attr('checked')){
            selected_items += $('#pk_' + i).val();
            if (i<how_many_selected-1)
                selected_items += '|';
        }
    }
    get_contract_detail_line(selected_items);
}

function get_contract_detail_line(selected_items){
    $.post("/invoices/contract/contract_detail_line_ajax/",
        {selected_items : selected_items},
        function(data){
            for (i in data){
                $('#table_details tr:last td:eq(1) input').val(data[i].fields.description);
                $('#table_details tr:last td:eq(2) input').val(data[i].fields.unity_cost);
                $('#table_details tr:last td:eq(3) input').val(data[i].fields.quantity);
                $('#table_details tr:last td:eq(4) input').val(data[i].fields.total);
                $('#table_details tr:last td:eq(6) input').val(data[i].pk);
                $('#table_details tr:last td:eq(8) input').val(data[i].fields.tax);
                $('#table_details tr:last td:eq(9) input').val(data[i].fields.retention);

                for (a=0;a<$('#contracts_table tr').length-1;a++)
                    if (parseInt($('#pk_' + a).val()) == data[i].pk){
                        $('#table_details tr:last td:eq(7) input').val($('#total_payed_' + a).val());
                        break;
                    }

                if (i<data.length-1){
                    add_new_row('table_details');
                    rename_hide_button('table_details');
                    add_focus_event(true);
                }
            }
            create_select_new_item();
            add_mouse_over_event();
        },
        "json"
    );
}

function get_contract_inf(contract_id){
    $.post("/invoices/contract/get_contract_inf/",
        {id : contract_id},
        function(data){
            $('#id_con-company')
                .val(data[0].fields.company)
                .attr('disabled', true)
            ;
            $('#id_con-project')
                .val(data[0].fields.project)
                .attr('disabled', true)
            ;

        },
        "json"
    );
}

function lock_fields(){
    $('.description input').attr('readonly', true);
    $('.unity_cost input').attr('readonly', true);
    $('.quantity input').attr('readonly', true);
    $('.taxes input').attr('readonly', true);
    $('#id_con-company').attr('disabled', true);
    $('#id_con-project').attr('disabled', true);
}

function create_select_new_item(){
    var existing_ids = '';
    len = $('#table_details tr').length-1;
    for (i=1; i<=len;i++){
        existing_ids += $('#id_details-' + (i-1) + '-contract_detail').val();
        if (i<len)
            existing_ids += '|';
    }

    $.post("/invoices/contract/new_contract_items/",
        {
            existing_ids : existing_ids,
            contract_id : $('#id_con-contract').val()
        },
        function(data){
            if (data.length>0){
                result = '<select id="avaiable_items"><option value="-1">' + $('#select_item').val() + '</option';
                for (i in data){
                    result += '<option value="' + data[i].pk + '">' + data[i].fields.description + '</option>'
                }
                result += '</select>';

                $('#for_avaiable_items').html(result);
                $('#avaiable').show();
                $('#avaiable_items')
                    .css('width',300)
                    .change(function(){
                        add_another_item();
                    })
                ;

            }
            else{
                $('#for_avaiable_items').html('');
                $('#avaiable').hide();
            }
        },
        "json"
    );
}

function add_another_item(){
    if ($('#avaiable_items').val()!=-1){
        add_new_row('table_details');
        add_focus_event(true);
        rename_hide_button('table_details');
        get_contract_detail_line(parseInt($('#avaiable_items').val()), 1, 1);
        $('#table_details tr:last td:eq(6) input').val(parseInt($('#avaiable_items').val()));
        create_select_new_item();
        add_mouse_over_event();
    }
    else
        $('#avaiable_items').val('-1');
}

function save_receipt(){
    $('#id_con-company').attr('disabled', false);
    $('#id_con-project').attr('disabled', false);
    save();
}