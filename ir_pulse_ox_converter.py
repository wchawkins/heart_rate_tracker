import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
#import plotly.plotly as py
import pandas as pd
import numpy as np
from scipy.signal import butter, lfilter, filtfilt
import csv

ir_data_frame = pd.read_csv('spo2art.csv')
ir_data_frame.columns = ['red', 'ir', 'green']

red = ir_data_frame.iloc[:, 0]
ir = ir_data_frame.iloc[:, 1]
green = ir_data_frame.iloc[:, 2]

Rwave = 650
IRwave = 950

logIR=np.log10(ir)
logRed=np.log10(red)
ratioR=(logRed*Rwave)/(logIR*IRwave)

spo2= 115-25*ratioR
rounded_spo2 = [ '%.2f' % elem for elem in spo2 ]

ir_data_frame['oxygen_saturation'] = rounded_spo2

oxygen_saturation_export = ir_data_frame.oxygen_saturation
oxygen_saturation_export.tail(10).to_csv('oxygen_saturation.csv')
#ir=ir[0:200]
# .667 Hz to 4 Hz
# fl = LowHR
# fh + high filter
# make sampling rate variable--- divided by to to make filter work
SR=22#Hz
LowHR =  2.0/3.0#Hz# = 40bpm
HighHR = 4.0 #Hz = 240 bpm
fL=LowHR/(SR/2)
fH=HighHR/(SR/2)
len_data = np.size(ir)

# Performing bandpass filter (removing DC offset)
b,a = butter(2,[fL,fH], btype='bandpass',output='ba') #2nd order (butterworth band-pass)
#print 'b and a'
#print a
#print b

filtered_time_data = filtfilt(b, a, ir, padtype = 'odd', padlen=3*(max(len(b),len(a))-1))
filtered_frequency_data = np.fft.fft(filtered_time_data) #converts from time domain to frequency domain by fft
p2=abs(filtered_frequency_data/len_data+1)
p1=p2[0:len_data/2+1]

np.savetxt("filtered_frequency_data.csv", filtered_frequency_data, delimiter=",")

max_value = np.max(p1)
indices = np.argmax(p1)
freq=np.arange((len_data/2),dtype=np.float);
freq=SR*freq/len_data
#print 'freq range'
#print freq
print "max_value"
print max_value
print "indices"
print indices
print 'HR Data'
print freq[indices]* 60 # HR in bpm
#print filtered_time_data[1:10]
ff=plt.figure(1)
len_data_p1 = np.size(p1)
xdata=np.zeros(len_data_p1)
#print(xdata)
i=0

for i in range(len_data_p1):
    #xdata[i]=float(i)*SR/len_data # frequency in Hz
    xdata[i]=float(i)*SR/len_data*60 # frequency in BPM

plt.plot(ir)
plt.ylabel('IR Intensity') #Look up
plt.xlabel("Sampling Rate")
plt.title('RAW IR DATA')
#plt.show()

fff=plt.figure(2)
plt.plot(filtered_time_data)
plt.title('DC FILTERED IR DATA')
plt.ylabel('IR Intensity')
plt.xlabel("Sampling Rate")

#plt.show()
ffff=plt.figure(3)
plt.plot(filtered_frequency_data)
plt.title('BUTTERWORTH-BAND PASSED 40-240 bpm FILTERED (non-normalized)')
plt.ylabel('Amplitude (unitless)')
plt.xlabel("Frequency Domain of Sampling Rate")
ffff=plt.figure(4)
plt.plot(xdata,p1)
plt.title('NORMALIZED FFT')
plt.ylabel('Amplitude')
plt.xlabel("Frequency (bpm)")
plt.show()

### Live CSV Visual
style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def animate(i):
    graph_data = open('spo2art.csv', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(x)
            ys.append(y)
    ax1.clear()
    ax1.plot(xs, ys)
    plt.xlabel("Time")
    plt.ylabel("Oxygen Saturation")
    plt.title('Oxygen Saturation')

ani = animation.FuncAnimation(fig, animate, interval = 1000)
plt.xlabel("Time")
plt.ylabel("Oxygen Saturation")
plt.title('Oxygen Saturation')
#plt.show()
#print SPo2
#print ir_data_frame

# interval = refresh rate in miliseconds
# https://www.youtube.com/watch?v=ZmYPzESC5YY
