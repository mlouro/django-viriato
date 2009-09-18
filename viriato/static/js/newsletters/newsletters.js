$(document).ready(function(){

// NEWSLETTER LIST
    // mouseover / mouseout todolist
    $(".newsletter-row").mouseover(function(){
        $(this).addClass("focused");
        $(this).children(".actions").removeClass("hidden");
    });
    $(".newsletter-row").mouseout(function(){
        $(this).removeClass("focused");
        $(this).children(".actions").addClass("hidden");
    });

// GROUP LIST
    // mouseover / mouseout todolist
    $(".group-row").mouseover(function(){
        $(this).addClass("focused");
        $(this).children(".actions").removeClass("hidden");
    });
    $(".group-row").mouseout(function(){
        $(this).removeClass("focused");
        $(this).children(".actions").addClass("hidden");
    });

// SUBSCRIBER LIST
    // mouseover / mouseout todolist
    $(".subscriber-row").mouseover(function(){
        $(this).addClass("focused");
        $(this).children(".actions").removeClass("hidden");
    });
    $(".subscriber-row").mouseout(function(){
        $(this).removeClass("focused");
        $(this).children(".actions").addClass("hidden");
    });

});