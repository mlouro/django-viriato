var tax, retention;

$(document).ready(function(){
    tax = $("#tax").val();
    retention = $("#retention").val();

    first_new_form = parseInt($("#id_details-INITIAL_FORMS").val());
    $("#id_details-" + first_new_form + "-tax").val(tax);
    $("#id_details-" + first_new_form + "-retention").val(retention);

    $("#hide_button_1").click(function(){
        show("hide_1");
    });

    $('#finals input').attr('readonly', 'true');
});

function change_image(event){
    local = $(button).attr("src").split('/');
    new_local = "";
    for (i=0;i<local.length-1;i++){
        new_local += local[i];
        if (i<local.length-1)
            new_local += '/';
    }
    if (event=="show")
        $(button).attr("src",new_local + "show.png");
    else
        $(button).attr("src",new_local + "hide.png");
}

function copy_tax_and_retention_values(table){
    nr_cols = $("#"+table + " tr").length-1;
    len = ($("#"+table + " tr td").length/nr_cols) - 1;
    $("#"+table + " tr:last td:eq("+(len-1)+") input").val(retention);
    $("#"+table + " tr:last td:eq("+(len-2)+") input").val(tax);
}

function show(id){
    button = "#hide_button_" + id.split('_')[1];
    $("."+id).show();
    $('.hide_headers').show();
    $(button).click(function(){
        hide(id);
    });
    change_image("hide", button);
}

function hide(id){
    button = "#hide_button_" + id.split('_')[1];
    $("."+id).hide();
    $('.hide_headers').hide();
    $(button).click(function(){
        show(id);
    });
    change_image("show", button);
}

function add_new_row(table){
    table_to_use = "#" + table;
    $(table_to_use + " tr:last td:eq(1) input").unbind("change");
    new_row_nr = $(table_to_use + " tr").length;
    $("#id_details-TOTAL_FORMS").val(new_row_nr);

    clonedRow = $(table_to_use + ' tr:last').clone();
    $(table_to_use).append(clonedRow);

    rename_cells(table);

    $(".stripes tr:last").mouseover(function(){
        $(this).addClass("over");
    }).mouseout(function(){
        $(this).removeClass("over");
    });

    remove_class_alt(table_to_use);
}

function rename_cells(table){
    table_to_use = '#' + table;
    new_row_nr = $("#id_details-TOTAL_FORMS").val()-1;
    columns_nr = $(table_to_use +" tr:last td").length-1;
    var ii=0;
    for (ii; ii<columns_nr; ii++){
        temp = $(table_to_use + " tr:last td:eq("+ii+") input").attr("id").split('-');
        new_id = temp[0] + '-' + new_row_nr + '-' + temp[2];

        temp = $(table_to_use + " tr:last td:eq("+ii+") input").attr("name").split('-');
        new_name = temp[0] + '-' + new_row_nr + '-' + temp[2];

        $(table_to_use + " tr:last td:eq("+ii+") input").attr("id", new_id).attr("name", new_name).val("");
    }
}

function add_mouse_over_event(){
    $(".stripes tr").mouseover(function(){
        $(this).addClass("over");
    }).mouseout(function(){
        $(this).removeClass("over");
    });
}

function remove_class_alt(table){
    len = $(table + " tr").length-1;
    if ($(table + " tr:eq("+len+")").attr("class"))
        $(table + " tr:eq("+len+")").removeClass("alt");
    else
        $(table + " tr:eq("+len+")").attr("class","alt");
}

function rename_hide_button(table){
    table = "#" + table;
    new_id_number = $(table + " tr").length-1;
    len = $(table + " tr td").length/new_id_number-1;
    $(table + " tr:last td:last img").attr("id","hide_button_"+new_id_number);
//     $(table + " tr:last td:eq(" + (len-1) + ")").attr("id","hide_"+new_id_number);

    new_class = "hide_" + new_id_number;
    old_class = "hide_" + (new_id_number-1);

    $(table+" tr:last td:eq("+(len-1)+")").removeClass(old_class).addClass(new_class);
    $(table+" tr:last td:eq("+(len-1)+")").attr("id",new_class);
    $(table+" tr:last td:eq("+(len-2)+")").removeClass(old_class).addClass(new_class);
    $(table+" tr:last td:eq("+(len-2)+")").attr("id",new_class);

    add_hide_event("#hide_button_" + new_id_number);
}

function add_hide_event(id){
    $(id).unbind("click");
    $(id).click(function(){
        show("hide_"+id.split('_')[2]);
    });
}

function remove_none_used_cols(table, initial_forms, total_forms, number_of_cols_to_check){
    deleted_rows = 0;
    o = document.getElementById(table);
    table = "#" + table;

    for (i=total_forms-1;i>=initial_forms;i--){
        if (o.rows[i+1].cells[0].firstChild.checked){
            o.deleteRow(i+1);
            deleted_rows++;
        }
        else{
            empty = true;
            for (check_col=1; check_col <= number_of_cols_to_check; check_col++){
                if ($(table + ' tr:eq('+(i+1)+') td:eq('+check_col+') input').val()!=""){
                    empty = false;
                    break;
                }
            }
            if (empty){
                o.deleteRow(i+1);
                deleted_rows++;
            }
        }
    }
    return deleted_rows;
}

function roundNumber(number,decimals) {
    var newString;// The new rounded number
    decimals = Number(decimals);
    if (decimals < 1) {
        newString = (Math.round(number)).toString();
    } else {
        var numString = number.toString();
        if (numString.lastIndexOf(".") == -1) {// If there is no decimal point
            numString += ".";// give it one at the end
        }
        var cutoff = numString.lastIndexOf(".") + decimals;// The point at which to truncate the number
        var d1 = Number(numString.substring(cutoff,cutoff+1));// The value of the last decimal place that we'll end up with
        var d2 = Number(numString.substring(cutoff+1,cutoff+2));// The next decimal, after the last one we want
        if (d2 >= 5) {// Do we need to round up at all? If not, the string will just be truncated
            if (d1 == 9 && cutoff > 0) {// If the last digit is 9, find a new cutoff point
                while (cutoff > 0 && (d1 == 9 || isNaN(d1))) {
                    if (d1 != ".") {
                        cutoff -= 1;
                        d1 = Number(numString.substring(cutoff,cutoff+1));
                    } else {
                        cutoff -= 1;
                    }
                }
            }
            d1 += 1;
        }
        if (d1 == 10) {
            numString = numString.substring(0, numString.lastIndexOf("."));
            var roundedNum = Number(numString) + 1;
            newString = roundedNum.toString() + '.';
        } else {
            newString = numString.substring(0,cutoff) + d1.toString();
        }
    }
    if (newString.lastIndexOf(".") == -1) {// Do this again, to the new string
        newString += ".";
    }
    var decs = (newString.substring(newString.lastIndexOf(".")+1)).length;
    for(var i=0;i<decimals-decs;i++) newString += "0";
    //var newNumber = Number(newString);// make it a number if you like
    return newString; // Output the result to the form field (change for your purposes)
}

function add_add_row_event(table){
    table_to_use = "#" + table;
    $(table_to_use + " tr:last td:eq(1) input").change(function(){
        if ($(this).val()!=""){
            add_new_row(table);
            copy_tax_and_retention_values(table);
            rename_hide_button(table);
            add_calculate_totals_event(table);
            add_calculate_row_total_event();//not global
            add_add_row_event('table_details');
        }
    });
}

function save(){
    initial_forms = parseInt($("#id_details-INITIAL_FORMS").val());
    total_forms = parseInt($("#id_details-TOTAL_FORMS").val());
    $("#id_details-TOTAL_FORMS").val(total_forms - parseInt(remove_none_used_cols("table_details", initial_forms, total_forms, 1)));
    document.getElementById("myForm").submit();
}