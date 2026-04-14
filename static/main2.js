Temp1 = document.getElementById("Temp1");
Temp2 = document.getElementById("Temp2");
Manual = document.getElementById("Manual");
State = document.getElementById("State");
avto = document.getElementById("avto");
min_lim = document.getElementById("min_lim");
max_lim = document.getElementById("max_lim");
room1 = document.getElementById("r_bed");
room2 = document.getElementById("r_kitch");
var relay=document.getElementById("relay_button");
var relay_status=0;

function upd_temp() {
    $.get("/getTemp", function(data, status){
        Temp1.innerHTML = data[0];
        Temp2.innerHTML = data[1];
        if(data[2])
            Manual.innerHTML = "ручний";
        else
            Manual.innerHTML = "автоматичний";
        if(data[3])
            State.innerHTML = "увімкнений";
        else
            State.innerHTML = "вимкнений";
        //relay_status=Number.parseInt(State);
		if(data[3]==false){
			relay.classList.remove('relay_on');
			relay.classList.add('relay_off');
			}
		else {
			relay.classList.remove('relay_off');
			relay.classList.add('relay_on');
			}

        //min_lim.innerHTML = data[4];
        //max_lim.innerHTML = data[5];
        //if (data[2]) avto.innerHTML = "1";
        //else avto.innerHTML = "0";
    });
}
setInterval(upd_temp, 1000);
function relay_inverse() {
    $.get("/relay_switch", function(data, status){
        State.innerHTML = data[0];
        //relay_status=Number.parseInt(State);
		if(data[0]==false){
			relay.classList.remove('relay_on');
			relay.classList.add('relay_off');
			relay_status=0;
			}
		else {
			relay.classList.remove('relay_off');
			relay.classList.add('relay_on');
			relay_status=1;
			}
    });
}
relay.addEventListener('click',relay_inverse);
			//document.addEventListener('DOMContentLoaded',relay_state);

//document.getElementById("sync_lim").onclick = function() {
//    $.get("/syncLimits", function(data, status){
//        min_lim.value = data[4];
//        max_lim.value = data[5];
//        avto.value = data[6];
//        room1 = data[6];
//        room2 = data[7];
//    });
//}
var chartData = [min_lim.value, max_lim.value, [Number(Temp1.innerHTML)], ['now'] ];


var ctx2 = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx2, {
    type: 'line',

    // The data for our dataset
    data: {
        labels: chartData[2],
        datasets: [{
            label: 'min',
            borderColor: 'rgb(132, 99, 255)',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            data: new Array(chartData[2].length).fill(chartData[0]),
            pointRadius: 0
        },{
            label: 'max',
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            data: new Array(chartData[2].length).fill(chartData[1]),
            pointRadius: 0
        },{
            label: 'temps',
            borderColor: 'rgb(100, 100, 100)',
            data: chartData[3]
        }

        ]
    },

    // Configuration options go here
    options: {
        animation: {
            duration: 0
        }
        //scales: {
            //xAxes: [{
                //type: 'time'
            //}]
        //}
    }
});

function getChartData() {
    $.get("/getChartData", function(data, status){
        chartData = data;
        var dates = [];
        for (var i = 0; i < data[2].length; i++)
            dates.push((new Date(data[2][i])).toUTCString().substr(5, 22));
        chart.data.labels = dates;
        chart.data.datasets[0].data = new Array(data[2].length).fill(data[0]);
        chart.data.datasets[2].data = data[3];
        chart.data.datasets[1].data = new Array(data[2].length).fill(data[1]);
        chart.update();
    });
}

getChartData();

setInterval(getChartData, 10000);
