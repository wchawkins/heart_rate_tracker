from converter import calculate_spo2_and_hr
from max3010X import MAX3010X
import time
import sender
import sys

# Global variables
SEND_DATA = False # Whether to enable remote transmission of data
WS = None # Websocket object
USERNAME = "" # Webapp username this sensor belongs to
SAMPLE_RATE = 100
SAMPLE_AVG = 4

def save_raw_data(red_buffer, ir_buffer, filename):
    with open(filename, 'a') as file:
        for i in range(len(red_buffer)):
            file.write("%d,%d\n" % (red_buffer[i], ir_buffer[i]))

def send_spo2_and_hr(spo2, hr):
    sender.send_data(WS, USERNAME, spo2, hr, 0)

def send_raw_data(red_buffer, ir_buffer):
    sender.send_raw_data(WS, USERNAME, red_buffer, ir_buffer)

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

        # Get all the samples from the sensor and add them to our buffer
        for i in range(available_samples):
            red, ir = m.read_from_fifo()
            red_buffer.append(red)
            ir_buffer.append(ir)
    
        # Wait until we have a decent sample size before running calculations
        if len(red_buffer) > 100:
            spo2, hr = calculate_spo2_and_hr(red_buffer, ir_buffer, SAMPLE_RATE, SAMPLE_AVG)
            print spo2, hr

            if SEND_DATA:
                send_spo2_and_hr(spo2, hr)
                # Only the send the latest raw data
                # send_raw_data(red_buffer[-available_samples:], ir_buffer[-available_samples:])

            # Delete the oldest 32 samples from the buffer, so we're
            # keeping our data fresh and not too big for the next round
            # of calculations 
            del red_buffer[:32]
            del ir_buffer[:32]

        save_raw_data(red_buffer, ir_buffer, raw_data_filename)

        # Since the sensor is sampling at 25 Hz (after averaging) and the FIFO
        # can hold 32 samples, waiting 1 second b/w reads should be fine.
        time.sleep(1)

if __name__ == "__main__":
    filename = sys.argv[1]

    # Making the ability to send data to the webapp optional for now
    if len(sys.argv) > 2:
        SEND_DATA = True
        webapp_address = sys.argv[2]
        USERNAME = sys.argv[3]
        WS = sender.join(webapp_address, USERNAME)

    main(filename)
