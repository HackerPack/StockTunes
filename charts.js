var funcc = {};

function toggle(el){
	var el = $(el).parent().find("input")[0];
	var player = $(el).parent().find("audio")[0];
    if(el.className!="pause")
    {
        el.src='img/pause.jpg';
        el.className="pause";
        player.play();
        funcc[player.className].start();
    }
    else if(el.className=="pause")
    {
        el.src='img/play.png';
        el.className="play";
        player.pause();
        funcc[player.className].stop();
    }
    return false;
}

function renderData(data){
	var name = data.name.substring(0, data.name.length - 4);
	var html = "\
		<div class='row' style='padding: 20px;margin: 20px;border: 1px solid #F35342;border-radius: 10px;margin-bottom: 40px;'>\
                <div class='row'>\
                    <div class='col-sm-2' style='text-align: center;margin-bottom: 10px;'>\
                        <input type='image' style='outline:none!important;width:50px; height:50px;opacity:0.7;border: 1px solid #F35342;border-width: 2px;border-radius: 15px;' src='img/play.png' class='play' onclick='toggle(this);'/>\
                        <audio onended='toggle(this);' id='player' src='"+data.download_url+"' class='"+name+"'></audio>\
                    </div>\
                    <div class='col-sm-10'>\
                        <label style='font-weight: 100;font-size: 50px;margin-top: -11px;text-transform: uppercase;'>"+name+"</label>\
                    </div>\
                </div>\
                <div class='row'>\
                    <canvas id='"+name+"' width='1118px' height='200px'></canvas>\
                </div>\
            </div>";
    return html;
}

$(function() {

	$.get("http://api.github.com/repos/HackerPack/StockTunes/contents/python/output").then(function(res){
        for(var i=0; i<res.length; i++){
        	var html = renderData(res[i]);
        	$("#container").append(html);
        	var name = res[i].name.substring(0, res[i].name.length - 4);
		    $.get("https://raw.githubusercontent.com/HackerPack/StockTunes/master/python/json/"+name+".json").then(function(res){
		        res = JSON.parse(res);
				var empty = [];
				var min = Math.min.apply(null, res.data);
				for(var j=0; j<res.data.length; j++){
					empty.push(null);
				}

				var tempDate = [];
				for(var j=0; j<res.date.length; j++){
					tempDate.push(res.date[j].substring(0, res.date[j].length - 5));
				}

				var data = {
			    labels: tempDate,
			    datasets: [
				        {
				            label: res.name,
				            fillColor: "rgba(220,220,220,0.5)",
				            strokeColor: "rgba(220,220,220,0.8)",
				            highlightFill: "rgba(220,220,220,0.75)",
				            highlightStroke: "rgba(220,220,220,1)",
				            data: res.data
				        },
				        {
				            label: res.name,
				            fillColor: "rgba(0,220,220,0.5)",
				            strokeColor: "rgba(0,220,220,0.8)",
				            highlightFill: "rgba(0,220,220,0.75)",
				            highlightStroke: "rgba(0,220,220,1)",
				            data: empty
				        }
			    	]
				};
				var ctx = $("#"+res.name).get(0).getContext("2d");
				var myLineChart = new Chart(ctx).Line(data, {"animation": false});
				
				funcc[res.name] = {};
				funcc[res.name].counter = 0;
				funcc[res.name].start = function(){
					var ll = res.len/res.data.length;
					funcc[res.name].id = window.setInterval(function(){
						myLineChart.datasets[1].points[funcc[res.name].counter].value = res.data[funcc[res.name].counter];
						myLineChart.update();
						funcc[res.name].counter = funcc[res.name].counter + 1;
					}, ll)
				}
				funcc[res.name].stop = function(){
					window.clearInterval(funcc[res.name].id);
				}
		    })        	
        }
    })
});

