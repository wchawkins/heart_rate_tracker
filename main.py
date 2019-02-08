from converter import calculate_spo2_and_hr
import max3010X
import time


def save_raw_data(red_buffer, ir_buffer):
    with open('red_ir.data', 'a') as file:
        for i in range(len(red_buffer)):
            print red_buffer[i], ir_buffer[i]
            file.write("%d,%d\n" % (red_buffer[i], ir_buffer[i]))
    # file.close()

SAMPLE_RATE = 100
SAMPLE_AVG = 4

def main():
    m = max3010X.MAX3010X()
    m.setup(sample_rate=SAMPLE_RATE, sample_avg=SAMPLE_AVG)

    while True:
        red_buffer = []
        ir_buffer = []
        samples_to_read = SAMPLE_RATE/SAMPLE_AVG

        for i in range(samples_to_read):
            red, ir = m.read_from_fifo()
            red_buffer.append(red)
            ir_buffer.append(ir)
    
        spo2, hr = calculate_spo2_and_hr(red_buffer, ir_buffer, SAMPLE_RATE, SAMPLE_AVG)
        # send_spo2_and_hr(spo2, hr)
        save_raw_data(red_buffer, ir_buffer)
        time.sleep(0.04)

if __name__ == "__main__":
    # main()
    m = max3010X.MAX3010X()
    m.setup(sample_rate=SAMPLE_RATE, sample_avg=SAMPLE_AVG)
    print m.get_read_pointer()
    print m.get_write_pointer()
    print m.read_fifo_config()
