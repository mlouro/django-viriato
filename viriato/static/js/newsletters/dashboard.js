function get_dashboard(newsletter_id){
    $.post("/newsletter/get_dashboard/",
        function(data){
            label=[];
            click=[];
            link=[];
            var info = JSON.parse(data);
            for (i in info){
                    label.push('%%.%%  ' +info[i].fields.label);
                    click.push(info[i].fields.click_count);
                    link.push(info[i].fields.link);
                };
            draw(label,click,link);
        },"json"
    );
}

//function draw(labels,clicks,links) {

//var r = Raphael("holder");
    //r.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";

    //r.g.text(320, 100, "Links").attr({"font-size": 20});

    ////var pie = r.g.piechart(320, 240, 100, [55, 20, 13, 32, 5, 1, 2, 10], {legend: ["%%.%% – Enterprise Users", "IE Users"], legendpos: "west", href: ["http://raphaeljs.com", "http://g.raphaeljs.com"]});
    //var pie = r.g.piechart(320, 240, 100, clicks, {legend: labels, legendpos: "east", href: links});
    //pie.hover(function () {
        //this.sector.stop();
        //this.sector.scale(1.1, 1.1, this.cx, this.cy);
        //if (this.label) {
            //this.label[0].stop();
            //this.label[0].scale(1.5);
            //this.label[1].attr({"font-weight": 800});
        //}
    //}, function () {
        //this.sector.animate({scale: [1, 1, this.cx, this.cy]}, 500, "bounce");
        //if (this.label) {
            //this.label[0].animate({scale: 1}, 500, "bounce");
            //this.label[1].attr({"font-weight": 400});
        //}
    //});
//};


function draw(labels,clicks,links) {
    var r = Raphael("holder"),
        fin = function () {
            this.flag = r.g.popup(this.bar.x, this.bar.y, this.bar.value || "0").insertBefore(this);
        },
        fout = function () {
            this.flag.animate({opacity: 0}, 300, function () {this.remove();});
        },
        fin2 = function () {
            var y = [], res = [];
            for (var i = this.bars.length; i--;) {
                y.push(this.bars[i].y);
                res.push(this.bars[i].value || "0");
            }
            this.flag = r.g.popup(this.bars[0].x, Math.min.apply(Math, y), res.join(", ")).insertBefore(this);
        },
        fout2 = function () {
            this.flag.animate({opacity: 0}, 300, function () {this.remove();});
        };
    r.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";

    //r.g.text(360, 30, "Links");
    

        r.g.text(320, 100, "Links Statistics").attr({"font-size": 20});
        
        var pie = r.g.piechart(320, 240, 100, clicks, {legend:labels, legendpos: "east", href: link});
        pie.hover(function () {
            this.sector.stop();
            this.sector.scale(1.1, 1.1, this.cx, this.cy);
            if (this.label) {
                this.label[0].stop();
                this.label[0].scale(1.5);
                this.label[1].attr({"font-weight": 800});
            }
        }, function () {
            this.sector.animate({scale: [1, 1, this.cx, this.cy]}, 500, "bounce");
            if (this.label) {
                this.label[0].animate({scale: 1}, 500, "bounce");
                this.label[1].attr({"font-weight": 400});
            }
        });

    

    
    
    
    
    
    

    //r.g.barchart(30, 60, 600, 320, clicks,{type: "soft"}).label(labels, true).hover(fin, fout).attr({stroke: "", fill:"hsb(.6, .6, .9)"});
    
    //r.g.hbarchart(330, 10, 300, 220, [[55, 20, 13, 32, 5, 1, 2, 10], [10, 2, 1, 5, 32, 13, 20, 55]], {stacked: true}).hover(fin, fout);
    //r.g.hbarchart(10, 250, 300, 220, [[55, 20, 13, 32, 5, 1, 2, 10], [10, 2, 1, 5, 32, 13, 20, 55]]).hover(fin, fout);
    //var c = r.g.barchart(330, 250, 300, 220, [[55, 20, 13, 32, 5, 1, 2, 10], [10, 2, 1, 5, 32, 13, 20, 55]], {stacked: true, type: "soft"}).hoverColumn(fin2, fout2);
    // c.bars[1].attr({stroke: "#000"});


    //var labels = ["Accessibility – ##", "Adobe – ##", "Advertising – ##", "Ajax – ##", "Android", "Apple", "Aptana", "Articles", "Atlas", "Bespin", "Book Reviews", "Bookmarklets", "Books", "Browsers", "Builds", "Business", "Calendar", "Canvas", "Cappuccino", "Chat", "Chrome", "Cloud", "ColdFusion", "Comet", "Component", "Conferences", "Contests", "CSS", "Database", "Debugging", "Design", "Dojo", "DWR", "Editorial", "Email", "Examples", "Ext", "Firefox", "Flash", "Framework", "Fun", "Games", "Gears", "Google", "GWT", "HTML", "IE", "Interview", "iPhone", "Java", "JavaScript", "jMaki", "jQuery", "JSON", "Library", "LiveEdit", "LiveSearch", "Mac", "Mapping", "Microformat", "Microsoft", "Mobile", "MooTools", "Mozilla", "Office", "Offline", "OpenAjax", "OpenWebPodcast", "Opera", "Performance", "Perl", "PHP", "Plugins", "Podcasts", "Portal", "Pragmatic Ajax", "Presentation", "Programming", "Prototype", "Python", "Qooxdoo", "Rails", "Recording", "Remoting", "RichTextWidget", "Roundup", "Ruby", "Runtime", "Safari", "Screencast", "Scriptaculous", "Security", "Server", "Showcase", "Social Networks", "Sound", "Standards", "Storage", "Survey", "SVG", "Testing", "The Ajax Experience", "TIBCO", "Tip", "Titanium", "Toolkit", "Tutorial", "UI", "Unobtrusive JS", "Usability", "Utility", "Video", "W3C", "Web20", "Widgets", "Workshop", "XmlHttpRequest", "Yahoo!"];
//r.g.barchart(700, 10, 170, 200, [[55, 20, 13, 32, 5, 1, 2, 10], [10, 2, 1, 5, 32, 13, 20, 55], [12, 20, 30]], 0, "sharp").hover(function () {
    //this.flag = r.g.flag(this.bar.x, this.bar.y, this.value || "0", 10);
//}, function () {
    //this.flag.animate({opacity: 0}, 100, function () {this.remove();});
//});


    //r.g.barchart(700, 200, 170, 150, [55, 20, 13, 32, 5, 1, 2, 10, 9, 15], false, "round", "25%").label(null, true).attr({stroke: "hsb(.6, .2, .9)", fill: "hsb(.6, .2, .9)", "fill-opacity": .35});


    //r.g.barchart(700, 420, 170, 100, [[55, 20, 13, 32, 5, 1, 2, 10]], 1).hover(function () {
        //this.flag = r.g.blob(this.bar.x + this.bar.w / 2, this.bar.y, this.value || "0", 30);
    //}, function () {
        //this.flag.animate({opacity: 0}, 100, function () {this.remove();});
    //});
    
    //var b = r.g.blob(320, 240, "12", 45).attr([{fill: "#fff", stroke: "#000"}, {fill: "#000", "font-size": 30}]).update();
    //var b = r.g.flag(320, 240, "12");
    
    //"a", 50, 50, 0, 0, 1, 100 + 100 * Math.cos(45 * Math.PI / 180), 100 - 100 * Math.sin(45 * Math.PI / 180)
    //.707

    //r.g.dropNote(400, 240, 444, "", 50, 45);
    //r.g.dropNote(320, 240, 12, 0, 0, -90);



    };
