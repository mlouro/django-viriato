function ShowPopup(hoveritem)
{
hp = document.getElementById("hoverpopup");

// Set position of hover-over popup
hp.style.top = hoveritem.offsetTop + 18;
hp.style.left = hoveritem.offsetLeft + 20;

// Set popup to visible
hp.style.visibility = "Visible";
}

function HidePopup()
{
hp = document.getElementById("hoverpopup");
hp.style.visibility = "Hidden";
}


// Other .js

$(document).ready(function(){
    $("#list-table tbody tr:odd").addClass("odd");
    
   $(function() {  
             $('#list-table tbody tr').mouseover(function() {  
                $(this).addClass('selectedRow');  
             }).mouseout(function() {  
                $(this).removeClass('selectedRow');  
             }).click(function() {  

             });  
   });
       
   $("#list-table thead tr input:checkbox").click(function(){

      if  (!$("#list-table thead tr input:checkbox").attr ("checked"))
      {
         $(".select_all").attr("checked",false);
      }      
      else
      {
         $(".select_all").attr("checked",true);
      }
   });
});
