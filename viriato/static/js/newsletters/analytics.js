function get_links(newsletter_id){
    $.post("/newsletter/get_links/",
        {newsletter_id: newsletter_id},
        function(data){
            for (i in data)
                alert (data[i].fields.slug);
                alert (data[i].fields.click_count)
        },
        "json"
    );
}
