import Chart from "chart.js"
import moment from "moment"
import socket from "./socket"

var ctx = document.getElementById("live-graph").getContext('2d');

function newDate(second) {
  return moment().add(second, 's').toDate();
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
      label: 'data',
      backgroundColor: color(chartColors.blue).alpha(0.5).rgbString(),
      borderColor: chartColors.blue,
      fill: false,
      data: [],
    }]
  },
  options: {
    responsive: true,
    title: {
      display: true,
      text: ''
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


window.liveChart = new Chart(ctx, config);

function plot(data) {
  console.log(data);

  var dataset = config.data.datasets[0].data;
  config.data.datasets[0].data.push({
    x: Date.now(),
    y: data
  });

  // Remove old data from the dataset
  if (dataset.length > 100) {
    console.log('length has reached 100')
    config.data.datasets[0].data.shift();
  }

  window.liveChart.update();
};

// Now that you are connected, you can join channels with a topic:
const meta = document.getElementById('metadata').dataset;
const username = meta.username;
const type = meta.type;
let token = '';

let channel = socket.channel("sensor:" + username, { params: { token: token } })

channel.on("new_data", payload => {
  console.log(payload)
  plot(payload[type])
})

channel.join()
  .receive("ok", resp => { console.log("Joined successfully", resp) })
  .receive("error", resp => { console.log("Unable to join", resp) })

