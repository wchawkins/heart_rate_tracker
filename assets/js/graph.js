import Chart from "chart.js"
import moment from "moment"
import socket from "./socket"

var spo2Ctx = document.getElementById("spo2-graph").getContext('2d');
var hrCtx = document.getElementById("hr-graph").getContext('2d');
var redCtx = document.getElementById("red-graph").getContext('2d');
var irCtx = document.getElementById("ir-graph").getContext('2d');

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

var redConfig = {
  type: 'line',
  data: {
    datasets: [{
      label: 'Red',
      backgroundColor: color(chartColors.red).alpha(0.5).rgbString(),
      borderColor: chartColors.red,
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

var irConfig = {
  type: 'line',
  data: {
    datasets: [{
      label: 'IR',
      backgroundColor: color(chartColors.red).alpha(0.5).rgbString(),
      borderColor: chartColors.red,
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
window.redChart = new Chart(redCtx, redConfig);
window.irChart = new Chart(irCtx, irConfig);

function randomScalingFactor() {
  const max = 250
  return Math.floor(Math.random() * Math.floor(max))
}

function plot(spo2, hr) {
  if (spo2Config.data.datasets.length > 0) {
    spo2Config.data.datasets[0].data.push({
      x: newDate(spo2Config.data.datasets[0].data.length + 1),
      y: spo2
    });
    hrConfig.data.datasets[0].data.push({
      x: newDate(hrConfig.data.datasets[0].data.length + 1),
      y: hr
    });

    console.log(spo2Config.data.datasets[0].data.length)

    // Remove old data from the dataset
    if (spo2Config.data.datasets[0].data.length > 100) {
      console.log('length has reached 100')
      spo2Config.data.datasets[0].data.shift();
      hrConfig.data.datasets[0].data.shift();
    }

    window.spo2Chart.update();
    window.heartRateChart.update();
  }
};

function plot_raw_data(red_buffer, ir_buffer) {
  // console.log("inside plot_raw_data");
  // console.log(red_buffer, ir_buffer);

  var redData = redConfig.data.datasets[0].data;
  var irData = irConfig.data.datasets[0].data;

  red_buffer.forEach(red => {
    redConfig.data.datasets[0].data.push({
      x: newDate(redData.length + 1),
      y: red
    });
  });

  ir_buffer.forEach(ir => {
    irConfig.data.datasets[0].data.push({
      x: newDate(irData.length + 1),
      y: ir
    })
  });

  // Remove old data from the dataset
  if (redData.length > 100) {
    console.log('length has reached 500')
    // redConfig.data.datasets[0].data.splice(0, red_buffer.length);
    // irConfig.data.datasets[0].data.splice(0, ir_buffer.length);
  }

  window.redChart.update();
  window.irChart.update();
}

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

const spo2Value = document.getElementById('spo2-value')
const hrValue = document.getElementById('hr-value')

channel.on("new_data", payload => {
  console.log(payload)
  plot(payload.spo2, payload.heart_rate)
  plot_raw_data(payload.red_buffer, payload.ir_buffer)

  // Update the value indicator
  spo2Value.innerText = Math.round(payload.spo2) + "%"
  hrValue.innerText = Math.round(payload.heart_rate) + " bpm"
})

channel.join()
  .receive("ok", resp => { console.log("Joined successfully", resp) })
  .receive("error", resp => { console.log("Unable to join", resp) })

