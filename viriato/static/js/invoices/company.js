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
            alert ('sda');
            node.removeClass("hidden");
            $(this).parent().addClass("hidden");
        }
        else
            alert ('das');
        return false;
    });
});