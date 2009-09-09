$(function () {
    var options = {
        lines: { show: true },
        points: { show: true },
        xaxis: { tickDecimals: 0, tickSize: 1 }
    };
    var data = [];
    var placeholder = $("#placeholder");
    
    $.plot(placeholder, data, options);

    
    // fetch one series, adding to what we got
    var alreadyFetched = {};
    
    $("input.fetchSeries").click(function () {
        var button = $(this);
        
        // find the URL in the link right next to us 
        var dataurl = button.siblings('a').attr('href');

        // then fetch the data with jQuery
        function onDataReceived(series) {
            // extract the first coordinate pair so you can see that
            // data is now an ordinary Javascript object
            var firstcoordinate = '(' + series.data[0][0] + ', ' + series.data[0][1] + ')';

            button.siblings('span').text('Fetched ' + series.label + ', first point: ' + firstcoordinate);

            // let's add it to our current data
            if (!alreadyFetched[series.label]) {
                alreadyFetched[series.label] = true;
                data.push(series);
            }
            
            // and plot all we got
            $.plot(placeholder, data, options);
         }
        
        $.ajax({
            url: dataurl,
            method: 'GET',
            dataType: 'json',
            success: onDataReceived
        });
    });


    // initiate a recurring data update
    $("input.dataUpdate").click(function () {
        // reset data
        data = [];
        alreadyFetched = {};
        
        $.plot(placeholder, data, options);

        var iteration = 0;
        
        function fetchData() {
            ++iteration;

            function onDataReceived(series) {
                // we get all the data in one go, if we only got partial
                // data, we could merge it with what we already got
                data = [ series ];
                
                $.plot($("#placeholder"), data, options);
            }
        
            $.ajax({
                // usually, we'll just call the same URL, a script
                // connected to a database, but in this case we only
                // have static example files so we need to modify the
                // URL
                url: "data-eu-gdp-growth-" + iteration + ".json",
                method: 'GET',
                dataType: 'json',
                success: onDataReceived
            });
            
            if (iteration < 5)
                setTimeout(fetchData, 1000);
            else {
                data = [];
                alreadyFetched = {};
            }
        }

        setTimeout(fetchData, 1000);
    });
});
