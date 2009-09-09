$(function () {
    var d1 = [];
    
    var d2 = [[0, 3], [4, 8], [8, 5], [9, 13]];
    
    $.plot($("#placeholder"), [
        {
            data: d1,
            lines: { show: false, fill: false }
        },
        {
            data: d2,
            bars: { show: true }
        },
        {

        },
        {

        },
        {

        }
    ]);
});


$(function () {
    $("#data_content").css({
        position: "absolute",
        left: "-9999em",
        top: "-9999em"
    });
});

window.onload = function () {
    // Grab the data
    var labels = [],
        data = [];
    $("#data_content tfoot th").each(function () {
        labels.push($(this).html());
    });
    $("#data_content tbody td").each(function () {
        data.push($(this).html());
    });
    
    // Draw
    var width = 800,
        height = 250,
        leftgutter = 30,
        bottomgutter = 20,
        topgutter = 20,
        colorhue = .6 || Math.random(),
        color = "hsb(" + [colorhue, 1, .75] + ")",
        r = Raphael("holder_content", width, height),
        txt = {font: '12px Fontin-Sans, Arial', fill: "#fff"},
        txt1 = {font: '10px Fontin-Sans, Arial', fill: "#fff"},
        txt2 = {font: '12px Fontin-Sans, Arial', fill: "#000"},
        X = (width - leftgutter) / labels.length,
        max = Math.max.apply(Math, data),
        Y = (height - bottomgutter - topgutter) / max;
    r.drawGrid(leftgutter + X * .5, topgutter, width - leftgutter - X, height - topgutter - bottomgutter, 10, 10, "#333");
    var path = r.path({stroke: color, "stroke-width": 4, "stroke-linejoin": "round"}),
        bgp = r.path({stroke: "none", opacity: .3, fill: color}).moveTo(leftgutter + X * .5, height - bottomgutter),
        frame = r.rect(10, 10, 100, 40, 5).attr({fill: "#000", stroke: "#474747", "stroke-width": 2}).hide(),
        label = [],
        is_label_visible = false,
        leave_timer,
        blanket = r.set();
    label[0] = r.text(60, 10, "24 hits").attr(txt).hide();
    label[1] = r.text(60, 40, "22 September 2008").attr(txt1).attr({fill: color}).hide();

    for (var i = 0, ii = labels.length; i < ii; i++) {
        var y = Math.round(height - bottomgutter - Y * data[i]),
            x = Math.round(leftgutter + X * (i + .5)),
            t = r.text(x, height - 6, labels[i]).attr(txt).toBack();
        bgp[i == 0 ? "lineTo" : "cplineTo"](x, y, 10);
        path[i == 0 ? "moveTo" : "cplineTo"](x, y, 10);
        var dot = r.circle(x, y, 5).attr({fill: color, stroke: "#000"});
        blanket.push(r.rect(leftgutter + X * i, 0, X, height - bottomgutter).attr({stroke: "none", fill: "#fff", opacity: 0}));
        var rect = blanket[blanket.length - 1];
        (function (x, y, data, lbl, dot) {
            var timer, i = 0;
            $(rect.node).hover(function () {
                clearTimeout(leave_timer);
                var newcoord = {x: +x + 7.5, y: y - 19};
                if (newcoord.x + 100 > width) {
                    newcoord.x -= 114;
                }
                frame.show().animate({x: newcoord.x, y: newcoord.y}, 200 * is_label_visible);
                label[0].attr({text: data + " hit" + ((data % 10 == 1) ? "" : "s")}).show().animate({x: +newcoord.x + 50, y: +newcoord.y + 12}, 200 * is_label_visible);
                label[1].attr({text: lbl + " September 2008"}).show().animate({x: +newcoord.x + 50, y: +newcoord.y + 27}, 200 * is_label_visible);
                dot.attr("r", 7);
                is_label_visible = true;
                r.safari();
            }, function () {
                dot.attr("r", 5);
                r.safari();
                leave_timer = setTimeout(function () {
                    frame.hide();
                    label[0].hide();
                    label[1].hide();
                    is_label_visible = false;
                    r.safari();
                }, 1);
            });
        })(x, y, data[i], labels[i], dot);
    }
    bgp.lineTo(x, height - bottomgutter).andClose();
    frame.toFront();
    label[0].toFront();
    label[1].toFront();
    blanket.toFront();
};
