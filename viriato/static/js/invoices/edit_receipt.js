$(document).ready(function(){

    initial_forms = parseInt($("#id_details-INITIAL_FORMS").val());
    total_forms = parseInt($("#id_details-TOTAL_FORMS").val());
    $("#id_details-TOTAL_FORMS").val(total_forms - parseInt(remove_none_used_cols("table_details", initial_forms, total_forms, 1)));
    rename_hide_buttons('table_details');
});

function receipt_is_not_editable(){
    $('input').attr('readonly', true);
    $('select').attr('disabled', true);
    $('.submit a').css('display', 'none');
 }

function rename_hide_buttons(table){
    table = "#" + table;
    nr_rows = $(table + " tr").length-1;
    len = $(table + " tr td").length/nr_rows;
    for (i=1;i<=nr_rows;i++){
        $(table + " tr:eq(" + i + ") td:last img").attr("id","hide_button_"+i);
        new_class = "hide_" + i;
        old_class = "hide_1";
        $(table+" tr:eq(" + i + ") td:eq("+(len-2)+")").removeClass(old_class).addClass(new_class);
        $(table+" tr:eq(" + i + ") td:eq("+(len-2)+")").attr("id",new_class);
        $(table+" tr:eq(" + i + ") td:eq("+(len-3)+")").removeClass(old_class).addClass(new_class);
        $(table+" tr:eq(" + i + ") td:eq("+(len-3)+")").attr("id",new_class);
        add_hide_event("#hide_button_" + i);
    }
}
