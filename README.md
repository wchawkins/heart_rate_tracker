# SpO2 Pi Python

This project is intended to run on a Raspberry Pi in order to read data from a
MAX30105 light sensor and calculate pulse oximetry and heart rate (and maybe more).

## Installing

Currently this project is using Python 2 and is intended to be ran on a Raspberry Pi.
The `requirements.txt` file lists the Python packages this project depends on.
You can try installing by doing `pip install -r requirements.txt`. Before doing so,
you may have to install Pandas with `sudo apt-get install python-pandas`.

## Usage

Run `python2 main.py filename` from the RPi.
This will save raw Red, IR light data to `filename` file.

Alternatively, if you want to send SpO2 and HR data to the web app, you can run
`python2 main.py filname wss://spo2-web.herokuapp.com username`, where username
is the username you signed-up with at https://spo2-web.herokuapp.com. Visit
https://spo2-web.herokuapp.com/graph to see the live data.

## Todo

- ~~Need some method to convert the raw light data to SpO2 and HR. Right now I made
defined a function called `calculate_spo2_and_hr` in converter.py that gets
called when you run main.py, but it just returns dummy data.~~

- I notice some jumps in the HR calculations. Maybe this is b/c we don't have a good signal or something? I noticed in [other HR calculation code](https://github.com/MaximIntegratedRefDesTeam/RD117_ARDUINO/blob/master/algorithm.cpp), they indicate whether the calculated SpO2 and HR values are valid, I'm guessing based off whether the signal is clear. Maybe we should think about this.

- ~~Need to implement the ability to send the SpO2 and HR measurements to the web
app. Currently, I have a placeholder in main.py called `send_spo2_and_hr(spo2, hr)`
for this purpose.~~
