from converter import calculate_spo2_and_hr
from max3010X import MAX3010X
import time
import sys

def save_raw_data(red_buffer, ir_buffer, filename):
    with open(filename, 'a') as file:
        for i in range(len(red_buffer)):
            # print red_buffer[i], ir_buffer[i]
            file.write("%d,%d\n" % (red_buffer[i], ir_buffer[i]))
    # file.close()

def send_spo2_and_hr(spo2, hr):
    print spo2, hr

SAMPLE_RATE = 100
SAMPLE_AVG = 4

def main(raw_data_filename):
    m = MAX3010X()
    # TODO: Fix the fact that sample_rate and sample_avg currently have
    # no effect - currently they're hardcoded to 100 and 4, respectively
    m.setup(sample_rate=SAMPLE_RATE, sample_avg=SAMPLE_AVG)

    red_buffer = []
    ir_buffer = []
    while True:

        # Check if we lost samples b/c we are too slow
        overflow_counter = m._read(0x05)[0]
        if overflow_counter > 0:
            print "Lost {} samples".format(overflow_counter)
        
        # Debugging the effective sample rate
        available_samples = m.available_samples()
        print "Reading {} samples".format(available_samples)

        for i in range(available_samples):
            red, ir = m.read_from_fifo()
            red_buffer.append(red)
            ir_buffer.append(ir)
    
        if len(red_buffer) > 100:
            spo2, hr = calculate_spo2_and_hr(red_buffer, ir_buffer, SAMPLE_RATE, SAMPLE_AVG)
            send_spo2_and_hr(spo2, hr)
        save_raw_data(red_buffer, ir_buffer, raw_data_filename)

        # Since the sensor is sampling at 25 Hz (after averaging) and the FIFO
        # can hold 32 samples, waiting 1 second b/w reads should be fine.
        time.sleep(1)

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
