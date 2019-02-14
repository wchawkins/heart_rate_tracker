# -*-coding:utf-8-*-

# this code is currently for python 2.7
from __future__ import print_function
from time import sleep

import RPi.GPIO as GPIO
import smbus

# i2c address-es
# not required?
I2C_WRITE_ADDR = 0xAE
I2C_READ_ADDR = 0xAF

# register addresses
REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01

REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03

REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08

REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C

REG_LED2_PA = 0x0D
REG_PILOT_PA = 0x10
REG_MULTI_LED_CTRL1 = 0x11
REG_MULTI_LED_CTRL2 = 0x12

REG_TEMP_INTR = 0x1F
REG_TEMP_FRAC = 0x20
REG_TEMP_CONFIG = 0x21
REG_PROX_INT_THRESH = 0x30
REG_REV_ID = 0xFE
REG_PART_ID = 0xFF

# currently not used
MAX_BRIGHTNESS = 255


class MAX3010X():
    """
    Represents the 30100 series of Maxim optical sesnsors. 
    Datasheet: https://cdn.sparkfun.com/assets/learn_tutorials/5/7/7/MAX30105_3.pdf
    """

    def __init__(self, channel=1, address=0x57, gpio_pin=7):
        """ Assumes that physical pin 7 (GPIO 4) is used as interrupt
        and the device is at 0x57 on channel 1 """ 
        print("Channel: {0}, address: {1}".format(channel, address))
        self.address = address
        self.channel = channel
        self.bus = smbus.SMBus(self.channel)
        self.interrupt = gpio_pin

        # set gpio mode
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.interrupt, GPIO.IN)

        self.reset()

        sleep(1)  # wait 1 sec

        # read & clear interrupt register (read 1 byte)
        reg_data = self._read(REG_INTR_STATUS_1)
        # self.setup()

    def _read(self, register, no_of_bytes=1):
        return self.bus.read_i2c_block_data(self.address, register, no_of_bytes)

    def _write(self, register, byte_values):
        return self.bus.write_i2c_block_data(self.address, register, byte_values)

    def setup(self, sample_rate=100, sample_avg=4):
        """
        This will setup the device with some default configuration.
        TODO: Allow sample_rate and sample_avg to be specified
        """
        # INTR setting
        # 0xc0 : A_FULL_EN and PPG_RDY_EN = Interrupt will be triggered when
        # fifo almost full & new fifo data ready
        self._write(REG_INTR_ENABLE_1, [0xc0])
        self._write(REG_INTR_ENABLE_2, [0x00])

        # FIFO_WR_PTR[4:0]
        self._write(REG_FIFO_WR_PTR, [0x00])
        # OVF_COUNTER[4:0]
        self._write(REG_OVF_COUNTER, [0x00])
        # FIFO_RD_PTR[4:0]
        self._write(REG_FIFO_RD_PTR, [0x00])

        """ FIFO Configuration - Register 0x08
        | B7  | B6  | B5 |      B4       | B3 | B2 | B1 | B0 |
        |-----|-----|----|---------------|----|----|----|----|
        | Sample Average | FIFO_ROLLOVER |    FIFO_A_FULL    |
        """
        self._write(REG_FIFO_CONFIG, [0b01011111])

        # 0x02 for read-only, 0x03 for SpO2 mode, 0x07 multimode LED
        self._write(REG_MODE_CONFIG, [0x03])
        # 0b 0010 0111
        # SPO2_ADC range = 4096nA, SPO2 sample rate = 100Hz, LED pulse-width = 411uS
        self._write(REG_SPO2_CONFIG, [0x27])

        # choose value for ~7mA for LED1
        self._write(REG_LED1_PA, [0x24])
        # choose value for ~7mA for LED2
        self._write(REG_LED2_PA, [0x24])
        # choose value fro ~25mA for Pilot LED
        self._write(REG_PILOT_PA, [0x7f])

    def shutdown(self):
        """
        Shutdown the device.
        """
        self._write(REG_MODE_CONFIG, [0x80])

    def reset(self):
        """
        Reset the device, this will clear all settings,
        so after running this, run setup() again.
        """
        self._write(REG_MODE_CONFIG, [0x40])

    def write_masked(self, register, mask, value):
        """
        Apply `mask` to current `register` with `value`
        and set it again.
        """
        # Get current register value
        current = self._read(register)
        # Zero (AND) the bits of interest using mask then
        # set them to value (OR)
        new = (current[0] & mask) | value
        self._write(register, new)

    def set_sample_rate(self, sample_rate):
        """
        sample_rate should be the number of samples per second
        the sensor should measure. It will be rounded down to
        one of the supported sample rate values.

        Register: 0x0A
        Bits: 2-4
        SR[2:0] | SAMPLES PER SECOND
        000     | 50
        001     | 100
        010     | 200
        011     | 400
        100     | 800
        101     | 1000
        110     | 1600
        111     | 3200
        """
        # binary value to set register for SR
        sr = 0b0
        if sample_rate < 100:
            # 50 sps
            sr = 0b000
        elif sample_rate < 200:
            # 100 sps
            sr = 0b001
        elif sample_rate < 400:
            # 200 sps
            sr = 0b010
        elif sample_rate < 800:
            # 400 sps
            sr = 0b011
        elif sample_rate < 1000:
            # 800 sps
            sr = 0b100
        elif sample_rate < 1600:
            # 1000 sps
            sr = 0b101
        elif sample_rate < 3200:
            # 1600 sps
            sr = 0b110
        else:
            # 3200 sps
            sr = 0b111

        # Shift it over since SR starts at 2nd bit of register
        sr <<= 2
        self.write_masked(REG_SPO2_CONFIG, 0b11100011, sr)

    def read_from_fifo(self):
        """
        This function will read the data register.
        """
        red_led = None
        ir_led = None

        # read 1 byte from registers (values are discarded)
        # reg_INTR1 = self._read(REG_INTR_STATUS_1)
        # reg_INTR2 = self._read(REG_INTR_STATUS_2)

        # read 6-byte data from the device
        d = self._read(REG_FIFO_DATA, 6)

        # mask MSB [23:18]
        red_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF
        ir_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF

        return red_led, ir_led

    def read_sequential(self, amount=100):
        """
        This function will read the red-led and ir-led `amount` times.
        This works as blocking function.
        """
        red_buf = []
        ir_buf = []
        for i in range(amount):
            while(GPIO.input(self.interrupt) == 1):
                # wait for interrupt signal, which means the data is available
                # do nothing here
                pass

            red, ir = self.read_from_fifo()

            red_buf.append(red)
            ir_buf.append(ir)

        return red_buf, ir_buf
    
    def read_ptr(self):
        """ Get the position of the FIFO read pointer """ 
        return self._read(REG_FIFO_RD_PTR)
    
    def write_ptr(self):
        """ Get the position of the FIFO write pointer """ 
        return self._read(REG_FIFO_WR_PTR)

    def available_samples(self):
        """ Get the number of sample available to be read from the FIFO """ 
        # TODO: Account for pointer wrap around, whatever
        # that means...
        return self.write_ptr() - self.read_ptr()

    def read_fifo(self):
        """
        Read all available samples from FIFO
        """
        num_available_samples = self.available_samples()
        for i in range(num_available_samples):
            print(self.read_from_fifo())
