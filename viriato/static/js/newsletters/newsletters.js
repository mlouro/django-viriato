$(document).ready(function(){

// NEWSLETTER LIST
    // mouseover / mouseout todolist
    $("h3.newsletter-row").mouseover(function(){
        $(this).addClass("focused");
        //$(this).children(".actions").removeClass("hidden");
    });
    $("h3.newsletter-row").mouseout(function(){
        $(this).removeClass("focused");
        //$(this).children(".actions").addClass("hidden");
    });

// GROUP LIST
    // mouseover / mouseout todolist
    $("h3.group-row").mouseover(function(){
        $(this).addClass("focused");
        //$(this).children(".actions").removeClass("hidden");
    });
    $("h3.group-row").mouseout(function(){
        $(this).removeClass("focused");
        //$(this).children(".actions").addClass("hidden");
    });

});



// DELETE IT WHEN NO LONGER NEEDED
    $(".task-complete.complete").attr("checked","checked");

    // toggle completion
    $(".task-complete").click(function(){
        var node = $(this);
        var task_id = node.attr("name").match("[0-9]+");
        var url = "/projects/" + $("#project_id").val() + "/task/ajax/complete/" + task_id + "/";

        function set_complete(node)
        {
            var children = node.children("ul li");
            $.each(children,function(){
                $(this).children(".task-row").addClass("complete");
                $(this).children(".task-row").children("label").children("input.task-complete").attr("checked",true);
                if ($(this).children("ul"))
                    set_complete($(this));
            });

        }

        function set_not_complete(node)
        {
            var parent_node = node.parent("ul").parent("li");
            if (parent_node.hasClass("task-li"))
            {
                parent_node.children(".task-row").removeClass("complete").children("label").children("input.task-complete").attr("checked",false).removeClass("complete");
                set_not_complete(parent_node);
            }
        }

        $.getJSON(url,function(data){
            if (data.complete == "True")
            {
                node.parent().parent().addClass("complete");
                set_complete(node.parent().parent().parent());
            }
            else
            {
                node.removeClass("complete");
                node.parent().parent().removeClass("complete");
                set_not_complete(node.parent().parent().parent());
            }
        });
    });

