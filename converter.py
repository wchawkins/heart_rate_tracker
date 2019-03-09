""" Used to convert raw Red/IR light data from the sensor to
pulse oximetry and heart rate data.
""" 

import math
import pandas as pd
import numpy as np
from scipy.signal import butter, lfilter, filtfilt
import csv

def calculate_spo2_and_hr(red_buffer, ir_buffer, sample_rate, sample_avg):
    red = np.array(red_buffer)
    ir = np.array(ir_buffer)
    
    # Typical wavelengths at 25 C (77 F) according to MAX30105 PDF
    Rwave = 660
    IRwave = 950
    
    logIR=np.log10(ir)
    logRed=np.log10(red)
    ratioR=(logRed*Rwave)/(logIR*IRwave)
    
    spo2= 115-25*ratioR
    rounded_spo2 = [ '%.2f' % elem for elem in spo2 ]
    
    #ir=ir[0:200]
    # .667 Hz to 4 Hz
    # fl = LowHR
    # fh + high filter
    # make sampling rate variable--- divided by to to make filter work
    SR = sample_rate / sample_avg # in Hz
    LowHR =  2.0/3.0#Hz# = 40bpm
    HighHR = 4.0 #Hz = 240 bpm
    fL = LowHR/(SR/2)
    fH = HighHR/(SR/2)
    len_data = np.size(ir)

    # Performing bandpass filter (removing DC offset)
    b, a = butter(2, [fL,fH], btype='bandpass', output='ba') #2nd order (butterworth band-pass)

    filtered_time_data = filtfilt(b, a, ir, padtype = 'odd', padlen=3*(max(len(b),len(a))-1))
    filtered_frequency_data = np.fft.fft(filtered_time_data) #converts from time domain to frequency domain by fft
    p2 = abs(filtered_frequency_data/len_data+1)
    p1 = p2[0:len_data/2+1]

    indices = np.argmax(p1)
    freq = np.arange((len_data/2), dtype=np.float)
    freq = SR*freq/len_data

    heart_rate = freq[indices]* 60 # HR in bpm
    
    return np.median(rounded_spo2), heart_rate

if __name__ == '__main__':
    pass