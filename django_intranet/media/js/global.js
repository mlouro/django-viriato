 $(document).ready(function(){


    $("#messages li a").click(function(){

        var message_count = $(this).parent().parent().length;

        if (message_count == 1)
            $(this).parent().parent().fadeOut("slow");
        else
            $(this).parent().fadeOut("slow");

        return false;
    });


 });

