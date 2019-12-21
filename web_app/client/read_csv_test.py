SENSOR_FILE = "/tmp/spo2.data"

def retrieve_sensor_data():
    with open(SENSOR_FILE, newline='') as file:
        while True:
            line = file.readline()
            if line:
                col = line.split(',')
                sample = {"red": col[0], "ir": col[1]}
                print(sample)
                # msg = {"topic": "sensor:sensorB", "event": "new_data", "payload": {"sample": sample}, "ref": None}

# retrieve_sensor_data()

def read_file_by_byte():
    with open('./lines') as f:
        f.seek(4)
        print(f.readline())


read_file_by_byte()
