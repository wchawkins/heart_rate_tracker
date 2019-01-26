import Chart from "chart.js"
import moment from "moment"
import socket from "./socket"

var ctx = document.getElementById("sensor-graph").getContext('2d');

function newDate(days) {
  return moment().add(days, 'd').toDate();
}

function newDateString(days) {
  return moment().add(days, 'd').format();
}

window.chartColors = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(201, 203, 207)'
};

var color = Chart.helpers.color;
var config = {
  type: 'line',
  data: {
    datasets: [{
      label: 'Red Light',
      backgroundColor: color('rgb(255, 99, 132)').alpha(0.5).rgbString(),
      borderColor: 'rgb(255, 99, 132)',
      fill: false,
      data: [],
    }, {
      label: 'IR Light',
      backgroundColor: color(window.chartColors.blue).alpha(0.5).rgbString(),
      borderColor: window.chartColors.blue,
      fill: false,
      data: []
    }]
  },
  options: {
    responsive: true,
    title: {
      display: true,
      text: 'Chart.js Time Point Data'
    },
    scales: {
      xAxes: [{
        type: 'time',
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Date'
        },
        ticks: {
          major: {
            fontStyle: 'bold',
            fontColor: '#FF0000'
          }
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'value'
        }
      }]
    }
  }
};

window.myLine = new Chart(ctx, config);

function randomScalingFactor() {
  const max = 250
  return Math.floor(Math.random() * Math.floor(max))
}

function plot(red, ir) {
  if (config.data.datasets.length > 0) {
    config.data.datasets[0].data.push({
      x: newDateString(config.data.datasets[0].data.length + 2),
      y: red
    });
    config.data.datasets[1].data.push({
      x: newDate(config.data.datasets[1].data.length + 2),
      y: ir
    });

    window.myLine.update();
  }
};

// Now that you are connected, you can join channels with a topic:
let channel = socket.channel("sensor:sensorB", {})

let messagesContainer = document.querySelector("#messages")

channel.on("new_data", payload => {
  console.log(payload)
  plot(payload.sample.red, payload.sample.ir)
  // let msgItm = document.createElement("li")
  // msgItm.innerText = `Red: ${payload.sample.red}, IR: ${payload.sample.ir}`
  // messagesContainer.appendChild(msgItm)
})

channel.join()
  .receive("ok", resp => { console.log("Joined successfully", resp) })
  .receive("error", resp => { console.log("Unable to join", resp) })

