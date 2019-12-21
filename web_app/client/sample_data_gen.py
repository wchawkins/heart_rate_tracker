""" Create sample/fake sensor data """
from random import randint
import time

sensor_file = "/tmp/spo2.data"

while True:
    with open(sensor_file, 'w') as file:
        sample = {"red": randint(1000, 10000), "ir": randint(1000, 10000)}
        # sample = {"red": 123, "ir": 1234}
        # file.write(str(sample['red']) + ',' + str(sample['ir']))
        print("{},{}".format(sample['red'], sample['ir']), file=file)
        time.sleep(1)
