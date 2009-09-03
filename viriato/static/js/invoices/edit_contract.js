$(document).ready(function(){
    nr_of_rows = $("#table_details tr").length-1;
    for (i=1; i<=nr_of_rows; i++)
        rename_hide_button_from_existing_lines(i);
//     $("#table_details tr:last td:eq(1) input").change(function(){
//         if ($("#table_details tr:last td:eq(1) input").val()!=""){
//             add_new_row("table_details");
//             copy_tax_and_retention_values("table_details");
//             rename_hide_button("table_details");
//         }
//     });
});

function rename_hide_button_from_existing_lines(i){
    $("#table_details tr:eq("+i+") td:eq() input")
    table = "#table_details";

    len = $(table + " tr td").length/ ($(table + " tr").length-1) -1;

    $(table + " tr:eq("+i+") td:last img").attr("id","hide_button_"+i);
    $(table + " tr:eq("+i+") td:eq(" + (len-1) + ")").attr("id","hide_"+i);
    
    new_class = "hide_" + i;
    old_class = "hide_1";
    
    $(table+" tr:eq("+i+") td:eq("+(len-1)+")").removeClass(old_class).addClass(new_class);
    $(table+" tr:eq("+i+") td:eq("+(len-1)+")").attr("id",new_class);
    $(table+" tr:eq("+i+") td:eq("+(len-2)+")").removeClass(old_class).addClass(new_class);
    $(table+" tr:eq("+i+") td:eq("+(len-2)+")").attr("id",new_class);
    
    add_hide_event("#hide_button_" + i);
}