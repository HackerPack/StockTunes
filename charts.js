$(function() {

	var data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
	        {
	            label: "My First dataset",
	            fillColor: "rgba(220,220,220,0.5)",
	            strokeColor: "rgba(220,220,220,0.8)",
	            highlightFill: "rgba(220,220,220,0.75)",
	            highlightStroke: "rgba(220,220,220,1)",
	            data: [65, 59, 80, 81, 56, 55, 40]
	        }
    	]
	};
    var ctx = $("#myChart").get(0).getContext("2d");
	// This will get the first returned node in the jQuery collection.
	var myLineChart = new Chart(ctx).Line(data);
	function fetchList(){
	    $.get("http://api.github.com/repos/HackerPack/StockTunes/contents/python/output").then(function(res){
	        console.log(res);
	        for (var x in res) {
	        	console.log(res[x].download_url);
	        }
	        return res;
	    })

	}
	var links=fetchList();
	var json={links};
	var ul = $('<ul>').appendTo('body');
    //var json = { items: ['item 1', 'item 2', 'item 3'] };
    $(json.links).each(function(index, item) {
        ul.append($(document.createElement('li')).text(item.download_url));
    });
});

