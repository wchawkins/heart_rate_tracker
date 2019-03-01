import Chart from "chart.js"
import moment from "moment"
import socket from "./socket"

var spo2Ctx = document.getElementById("spo2-graph").getContext('2d');
var hrCtx = document.getElementById("hr-graph").getContext('2d');

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

var spo2Config = {
  type: 'line',
  data: {
    datasets: [{
      label: 'SpO2',
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

var hrConfig = {
  type: 'line',
  data: {
    datasets: [{
      label: 'Heart Rate',
      backgroundColor: color('rgb(255, 99, 132)').alpha(0.5).rgbString(),
      borderColor: 'rgb(255, 99, 132)',
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

window.spo2Chart = new Chart(spo2Ctx, spo2Config);
window.heartRateChart = new Chart(hrCtx, hrConfig);

function randomScalingFactor() {
  const max = 250
  return Math.floor(Math.random() * Math.floor(max))
}

function plot(spo2, hr) {
  if (spo2Config.data.datasets.length > 0) {
    spo2Config.data.datasets[0].data.push({
      x: newDateString(spo2Config.data.datasets[0].data.length + 2),
      y: spo2
    });
    hrConfig.data.datasets[0].data.push({
      x: newDate(hrConfig.data.datasets[0].data.length + 2),
      y: hr
    });

    window.spo2Chart.update();
    window.heartRateChart.update();
  }
};

// Now that you are connected, you can join channels with a topic:
let username = '';
let token = '';

const metas = document.getElementsByTagName('meta');
for (let i = 0; i < metas.length; i++) {
  const name = metas[i].getAttribute('name');
  const content = metas[i].getAttribute('content');
  switch (name) {
    case 'username':
      username = content;
      break;
    case 'channel_token':
      token = content;
  }
}
let channel = socket.channel("sensor:" + username, { params: { token: token } })

let messagesContainer = document.querySelector("#messages")

channel.on("new_data", payload => {
  console.log(payload)
  plot(payload.spo2, payload.hr)
  // let msgItm = document.createElement("li")
  // msgItm.innerText = `Red: ${payload.sample.red}, IR: ${payload.sample.ir}`
  // messagesContainer.appendChild(msgItm)
})

channel.join()
  .receive("ok", resp => { console.log("Joined successfully", resp) })
  .receive("error", resp => { console.log("Unable to join", resp) })

