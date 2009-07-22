// class widget.media
widget.media = new Object();

widget.media.__jquery_obj = '';


widget.media.id = function(value){if (value)this.__media_id = value;return this.__media_id; }
widget.media.__id = '';

widget.media.caption = function(value){if (value)this.__caption = value;return this.__caption; }
widget.media.__caption = '';

widget.media.template_tag = function(){
    return '{% media_insert '+ widget.media.id() + ' "'+ widget.media.caption() +'" %}'
}


/* loads properties from jquery_obj html block */
widget.media.load = function(jquery_obj)
{
    widget.media.__jquery_obj = jquery_obj;
    var template_tag = widget.media.__jquery_obj.children(".widget-code").text();

    /* get caption */
    re = new RegExp('{% media_insert ([0-9]{0,}) "([a-zA-Z]{0,})" %}');
    console.log(template_tag);
    var matches = template_tag.match(re);
    if (matches)
    {
        widget.media.id(matches[1]);
        widget.media.caption(matches[2]);
    }
};


/* public call to bring up the editor screen */
widget.media.edit = function()
{
    var url = $("#widget-media-options .widget-edit").attr("href");
    widget.lightbox(url,widget.media.__edit_callback);
    return false;
};

/* returns selected option from align select box */
widget.media.__check_align = function()
{
    $.each($("#media-align option"),function(i,val){
        var option = $(val);
        if ($("#media-tag .widget-block").hasClass(option.val()))
            $("#media-align option[value="+ option.val() +"]").attr("selected","selected");
    });
};

widget.media.__set_align_class = function()
{
    $.each($("#media-align option"),function(i,val){
        widget.media.__jquery_obj.removeClass($(val).val());
    });
    widget.media.__jquery_obj.addClass($("#media-align option:selected").val());
}



/*
callback for when media editor pop'ups
handles option clicks and save button
*/
widget.media.__edit_callback = function()
{
    widget.media.__jquery_obj.clone().appendTo("#media-tag");

    $("#widget-media-caption").val(widget.media.caption());
    $("#template-tag").val(widget.media.template_tag());

    widget.media.__check_align();

    $.each($("#media-align option"),function(i,val){
        $("#media-tag .widget-block").removeClass($(val).val());
    });

    /* change caption on template tag keyup event */
    $("#widget-media-caption").keyup(function(){
        widget.media.caption($(this).val());
        $("#template-tag").val(widget.media.template_tag());
    });

    $("#lb-block-save").click(function(){
        var img_src = $("#media-tag .widget-media-block img").attr("src");
        var img_tag = $("#media-tag .widget-code").text();

        widget.media.__jquery_obj.children("img").attr("src",img_src);
        widget.media.__jquery_obj.children(".widget-code").text(widget.media.template_tag());

        $.each($("#media-align option"),function(i,val){
            widget.media.__jquery_obj.removeClass($(val).val());
        });

        widget.media.__set_align_class();

        tb_remove();
    });

};