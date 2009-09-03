$(document).ready(function(){
    rename_hide_buttons('table_details');
    initial_forms = parseInt($("#id_details-INITIAL_FORMS").val());
    total_forms = parseInt($("#id_details-TOTAL_FORMS").val());
    $("#id_details-TOTAL_FORMS").val(total_forms - parseInt(remove_none_used_cols("table_details", initial_forms, total_forms, 1)));
});

function receipt_is_not_editable(){
    $('input').attr('readonly', true);
    $('select').attr('disabled', true);
    $('.submit a').css('display', 'none');
 }

function rename_hide_buttons(table){
    table = "#" + table;
    nr_rows = $(table + " tr").length-1;

    for (i=1;i<=nr_rows;i++){
        len = $(table + " tr td").length/nr_rows;
        $(table + " tr:eq(" + i + ") td:last img").attr("id","hide_button_"+i);
//         $(table + " tr:eq(" + i + ") td:eq(" + (len-1) + ")").attr("id","hide_"+i);

        new_class = "hide_" + i;
        old_class = "hide_" + (i-1);
        $(table+" tr:eq(" + i + ") td:eq("+(len-1)+")").removeClass(old_class).addClass(new_class);
        $(table+" tr:eq(" + i + ") td:eq("+(len-1)+")").attr("id",new_class);
        $(table+" tr:eq(" + i + ") td:eq("+(len-2)+")").removeClass(old_class).addClass(new_class);
        $(table+" tr:eq(" + i + ") td:eq("+(len-2)+")").attr("id",new_class);

//         $(table+" tr:last td:eq("+(len-1)+")").removeClass(old_class).addClass(new_class);
//         $(table+" tr:eq(last) td:eq("+(len-1)+")").attr("id",new_class);
//         $(table+" tr:last td:eq("+(len-2)+")").removeClass(old_class).addClass(new_class);
//         $(table+" tr:eq(last) td:eq("+(len-2)+")").attr("id",new_class);

        add_hide_event("#hide_button_" + i);
    }
}
