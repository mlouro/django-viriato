$(document).ready(function(){


    // mouseover / mouseout todolist
    $("div.milestone-details").mouseover(function(){
        $(this).addClass("focused");
        $(this).children(".actions").removeClass("hidden");
    });
    $("div.milestone-details").mouseout(function(){
        $(this).removeClass("focused");
        $(this).children(".actions").addClass("hidden");
    });


    // remove todo list
    $("#todolist .milestone .todo-details .actions .delete").click(function(){
        var todo_id = $(this).parent().parent().children(":first").val();
        jQuery.post("/todo/ajax/removetodo/", { id : todo_id } );
        $(this).parent().parent().parent().remove();

        return false;
    });

});
