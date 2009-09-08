$(document).ready(function(){
    $('#have_contract')
        .jqm({
            modal: true,
            overlay: 88,
            onHide: function(h) {
                h.w.fadeOut(888); // hide window
                h.o.remove(); // remove overlay
            },
        })
    ;


});

function add_close_event_to_buttons(){
    $('#have_contract')
        .jqmAddClose($('#jqmOk'))
        .jqmAddClose($('#jqmClose'))
    ;
}