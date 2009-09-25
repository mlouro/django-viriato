window.onload = draw;


    
$(function () {
    $("#data").css({
        position: "absolute",
        left: "-9999em",
        top: "-9999em"
    });
});


function draw() {
    // Grab the data
    var labels = [],
        data = [];
    $("#data tfoot th").each(function () {
        labels.push($(this).html());
    });
    $("#data tbody td").each(function () {
        data.push($(this).html());
    });
    

    
    // Draw
    var width = 800
        rightgutter = 20,
        height = 250,
        leftgutter = 30,
        bottomgutter = 20,
        topgutter = 25,
        colorhue = .7 || Math.random(),
        color = "hsb(" + [colorhue, 1, .75] + ")",
        r = Raphael("holder", width, height),
        txt = {"font": '12px "Arial"', stroke: "none", fill: "#000"},
        txt1 = {"font": '9px "Arial"', stroke: "none", fill: "#000"},
        X = (width - leftgutter - rightgutter) / labels.length,
        max = Math.max.apply(Math, data),
        Y = (height - bottomgutter - topgutter) / data.length;
    r.path({stroke: "#036"}).moveTo(leftgutter, topgutter-20).lineTo(leftgutter, height-bottomgutter);
      r.path({stroke: "#036"}).moveTo(leftgutter, height-bottomgutter).lineTo(width, height-bottomgutter);
    var frame = r.rect(10, 10, 50, 20, 5).attr({fill: "#888", stroke: "#474747", "stroke-width": 2}).hide(),
        is_label_visible = false,
        leave_timer,
        blanket = r.set(),
            bar_label = r.text(60, 40, "22 September 2008").attr(txt1).hide(),
            t0 = r.text(leftgutter-14, height-25, 0).attr(txt).toBack();
   
    for(var i = 0, ii = labels.length; i < ii; i++)
        {
            var y = height - bottomgutter - data[i]/ max * (height - bottomgutter - topgutter),
          x = Math.round(leftgutter + X * (i+1)),
          ty = r.text(leftgutter - 14, topgutter + i * Y, Math.round(max/data.length*(ii-i))).attr(txt).toBack(),
          tx = r.text(x-30, height - 6, labels[i]).attr(txt).toBack(),         
          bar = r.rect(x-50, y, X-20, data[i]/ max * (height - bottomgutter - topgutter)).attr({fill: color, stroke: color});   
           
            blanket.push(r.rect(x-50, 20, X-20, height - bottomgutter - topgutter).attr({stroke: "#fff", fill: "#000", opacity: 0}));
      var rect = blanket[i];
      
      (function (x, y, data, label, bar) {
            var timer, i = 0;
            $(rect.node).hover(function () {
                clearTimeout(leave_timer);
                var newcoord = {x: x-48, y: y-40};
                if (newcoord.y - 20 < 0) {
                    newcoord.y += 16;
                }
                bar.attr({opacity: .3});   
                frame.show().animate({x: newcoord.x, y: newcoord.y}, 200 * is_label_visible);
               // bar_label.show();
                   bar_label.attr({text: label}).show().animate({x: newcoord.x + 25, y: newcoord.y + 10}, 200 * is_label_visible);
                bar_label.toFront();
                is_label_visible = true;
                r.safari();
            }, function () {
                    bar.attr({opacity: 1});   
                r.safari();
                leave_timer = setTimeout(function () { 
                    frame.hide();
                    bar_label.hide();
                    is_label_visible = false;
                    r.safari();
                }, 1);
            });
        })
            (x, y, data[i], data[i], bar);
        }  
};


function get_links(newsletter_id){
    $.post("/newsletter/get_links/",
        {newsletter_id: newsletter_id},
        function(data){
            for (i in data){
                label.push(data[i].fields.slug);
                click.push(data[i].fields.click_count);
                //alert(label[i]);
                //alert(click[i]);
                }
        },
        "json"
    );
}