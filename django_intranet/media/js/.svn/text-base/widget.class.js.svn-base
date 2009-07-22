var widget = {

    text_edit : function(widget_obj){

        function callback_init()
        {
            $("#textarea-editor").val(widget_obj.children(".widget-content").html());
            widget.init_editor();

            if (widget_obj.hasClass("clear"))
                $("input[value='clear']").attr("checked","checked");
            else
                $("input[value='']").attr("checked","checked");

            $("#lb-block-save").click(function(){
                var content = $("#textarea-editor_ifr").contents().find("body").html();
                var clear_opt = $("input[name='wrap_text']:checked").val();
                if (clear_opt)
                    widget_obj.addClass("clear");
                else
                    widget_obj.removeClass("clear");
                widget_obj.children(".widget-content").html(content);
                tb_remove();
            });

        };

        var url = $("#widget-text-options a.widget-edit").attr("href");
        widget.lightbox(url,callback_init);
        return false;
    },

    /* add a template to story */
    add_to_story : function(){

        $(".widget-add").click(function(){
            var widget_block = $(this).parent().children(".widget-html");
            var story_content = $(".tab-contents .tab:not(.hidden)").html();

            story_content += widget_block.html();

            $(".tab-contents .tab:not(.hidden)").html(story_content);

            return false;
        });
    },



    /* show a generic lightbox with a callback_init function as parameter */
    lightbox : function(url,callback_init) {

        tb_show(null,url,false,callback_init);
        return false;
    },

    /* init Rich Text Editor */
    init_editor : function(){

        // O2k7 skin (silver)
        tinyMCE.init({
            // General options
            mode : "exact",
            elements : "textarea-editor",
            theme : "advanced",
            skin : "o2k7",
            skin_variant : "black",
            width : "525",
            height :"350",
            plugins : "safari,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,inlinepopups",

            // Theme options
            theme_advanced_buttons1 : "newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontsizeselect",
            theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,cleanup,help,code",
            theme_advanced_buttons3 : "tablecontrols,|,hr,removeformat,visualaid,|,fullscreen",
            theme_advanced_toolbar_location : "top",
            theme_advanced_toolbar_align : "left",
            theme_advanced_statusbar_location : "bottom",
            theme_advanced_resizing : false,
            /*
            save_callback : "widget.save_text_editor",
            */


            // Example content CSS (should be your site CSS)
            /*
            content_css : "css/content.css",
            */

            // Drop lists for link/image/media/template dialogs
            /*
            template_external_list_url : "lists/template_list.js",
            external_link_list_url : "lists/link_list.js",
            external_image_list_url : "lists/image_list.js",
            media_external_list_url : "lists/media_list.js",
            */
            // Replace values for the template plugin
            template_replace_values : {
                username : "Some User",
                staffid : "991234"
            }

        });
    }
};