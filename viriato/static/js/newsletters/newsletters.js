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