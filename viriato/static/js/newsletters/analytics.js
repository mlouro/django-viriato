function get_links(newsletter_id){
    $.post("/newsletter/get_links/",
        {newsletter_id: newsletter_id},
        function(data){
            label=[];
            click=[];
            link=[];
            for (i in data){
                if (data[i].fields.label  != "unsubscribe"){
                    label.push('%%.%% ' +(data[i].fields.label));
                    click.push(data[i].fields.click_count);
                    link.push(data[i].fields.link);
                    };
                };
            draw(label,click,link);
        },"json"
    );
}

function draw(labels,clicks,links) {

var r = Raphael("holder");
          r.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";
          
          r.g.text(320, 100, "Links").attr({"font-size": 20});
          
          //var pie = r.g.piechart(320, 240, 100, [55, 20, 13, 32, 5, 1, 2, 10], {legend: ["%%.%% – Enterprise Users", "IE Users"], legendpos: "west", href: ["http://raphaeljs.com", "http://g.raphaeljs.com"]});
          var pie = r.g.piechart(320, 240, 100, clicks, {legend: labels, legendpos: "east", href: links});
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
