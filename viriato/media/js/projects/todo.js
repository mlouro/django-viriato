$(document).ready(function(){

    $(".additem").click(function(){

        var addform = $("#todo-itemform").appendTo($(this).parent().parent()).removeClass("hidden").addClass("add");

        $(".todo .add.hidden").removeClass("hidden");
        $(this).parent().addClass("hidden");

        return false;
    });


    $(".todoitem-cancel").click(function(){
        $(".todo .add.hidden").removeClass("hidden");
        $("#todo-itemform").addClass("hidden");
        return false;
    });



    // mouseover / mouseout todolist
    $("div.todo-details").mouseover(function(){
        $(this).children(".actions").removeClass("hidden");
    });
    $("div.todo-details").mouseout(function(){
        $(this).children(".actions").addClass("hidden");
    });


    // remove todo list
    $("#todolist .milestone .todo-details .actions .delete").click(function(){
        var todo_id = $(this).parent().parent().children(":first").val();
        jQuery.post("/todo/ajax/removetodo/", { id : todo_id } );
        $(this).parent().parent().parent().remove();

        return false;
    });



    // mouseover / mouseout todoitem
    $(".todo-itemlist li").mouseover(function(){
        $(this).children(".actions").removeClass("hidden");
    });
    $(".todo-itemlist li").mouseout(function(){
        $(this).children(".actions").addClass("hidden");
    });

    // remove todo item
    $(".todo-itemlist li .actions .delete").click(function(){
        var todo_id = $(this).parent().parent().children(":first").val();
        jQuery.post("/todo/ajax/removeitem/", { id : todo_id } );
        $(this).parent().parent().remove();

        return false;
    });


    $(".todoitem-add").click(function(){

        $(".error").remove();

        if ($(this).parent().parent().children(":first").children("input[name=title]").val().length > 0)
        {
            $(".todoitem-add").addClass("hidden").before('<img class="ajax-loader" src="http://media.zolba.com/images/ajax/ajax-loader-gray.gif"');

            var fields = new Object();
            $("#todo-itemform input[type=text],#todo-itemform select").each(function(){
                fields[this.name] = this.value;
            });

            fields.todo = $(this).parent().parent().parent().children(":first").children(":first").val();

            jQuery.getJSON("/todo/ajax/additem/", fields, function(data){

                // remove ajax loader and show save button
                $(".todoitem-add").prev().remove();
                $(".todoitem-add").removeClass("hidden");
                // empty the input value
                $("#todo-itemform .field:first input").val("");

                // add field to list
                var todo_list = $("#todo-itemform").parent().children("ul.todo-itemlist");
                var todo_li_item = todo_list.children(":first").clone(true);
                todo_li_item.children("input").val(data.id);
                todo_li_item.children("span.title").text(data.title);
                todo_li_item.children("span.assigned_to").text(data.assigned_username);
                todo_li_item.removeClass("hidden");
                todo_li_item.appendTo(todo_list);
            });
        }
        else
        {
            $("#todo-itemform .field:first").append('<p class="error">The title must have more than three chars</p>');
        }
        return false;
    });

});
