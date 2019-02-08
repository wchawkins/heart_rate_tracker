""" Basically copy of algorithm from ir_pulse_ox_converter.py,
just not using numpy or pandas in order to quickly test on Pi
without having to download those packages. 
""" 

import math

def calculate_spo2_and_hr(red_buffer, ir_buffer, sample_rate, sample_avg):
    # TODO: Implement calculation of heart rate and O2 sat 

    # Typical wavelengths at 25 C (77 F) according to MAX30105 PDF
    # Rwave = 660
    # IRwave = 950
    
    # logIR = math.log10(ir)
    # logRed = math.log10(red)
    # ratioR = (logRed*Rwave)/(logIR*IRwave)
    # spo2 = 110-25*ratioR

    fake_spo2 = 98
    fake_hr = 75

    return fake_spo2, fake_hr

if __name__ == '__main__':
    pass