$(document).ready(function(){

    $("#show_extra_information").click(function(){
        var node = $("#extra_information");
        if (node.hasClass("hidden"))
        {
            node.removeClass("hidden");
            $(this).parent().addClass("hidden");
        }
        return false;
    });

    $("#show_contact_information").click(function(){
        var node = $("#contact_information");
        if (node.hasClass("hidden"))
        {
            node.removeClass("hidden");
            $(this).parent().addClass("hidden");
        }
        return false;
    });

    $('#show_emails').click(function(){
        show_div('emails');
    });

    $('#show_addresses').click(function(){
        show_div('addresses');
    });

    $('#show_phones').click(function(){
        show_div('phones');
    });

    $('#show_websites').click(function(){
        show_div('websites');
    });

    $('#show_ims').click(function(){
        show_div('ims');
    });

    $('#show_email_settings').click(function(){
        show_div('email_settings');
    });

});

function show_div(id){
    $('#' + id).show('slow');
    src = $('#show_' + id).attr('src').split('/');
    new_src = "";
    for (i=0;i<src.length-1;i++)
        new_src += src[i] + '/';
    new_src += 'hide_div.png';
    $('#show_' + id)
        .unbind()
        .attr('src', new_src)
        .attr('alt', 'hide')
        .click(function(){ hide_div(id)})
    ;
}

function hide_div(id){
    $('#' + id).hide('slow');
    src = $('#show_' + id).attr('src').split('/');
    new_src = "";
    for (i=0;i<src.length-1;i++)
        new_src += src[i] + '/';
    new_src += 'show_div.png';
    $('#show_' + id)
        .unbind()
        .attr('src', new_src)
        .attr('alt', 'show')
        .click(function(){ show_div(id)})
    ;
}