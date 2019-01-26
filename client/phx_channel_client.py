import argparse
import asyncio
import csv
import websockets
import json
import time

# SENSOR_FILE = "/tmp/spo2.data"
# WS_ADDRESS = 'ws://127.0.0.1:4000/socket/websocket'


async def retrieve_sensor_data(sensor_file):
    with open(sensor_file, newline='') as file:
        line = 'asdf'
        # while True:
        line = file.readline()
        if line:
            col = line.split(',')
            sample = {"red": col[0], "ir": col[1]}
            print(sample)
            msg = {"topic": "sensor:sensorB", "event": "new_data",
                   "payload": {"sample": sample}, "ref": None}
            return msg
        else:
            time.sleep(0.5)

async def retrieve_sensor_data2(sensor_file):
    with open(sensor_file, newline='') as file:

        def create_msgs_from_lines(lines):
            msgs = []
            for line in lines:
                col = line.split(',')
                sample = {"red": col[0], "ir": col[1]}
                msg = {"topic": "sensor:sensorB", "event": "new_data",
                      "payload": {"sample": sample}, "ref": None}
                msgs.append(msg)
            return msgs

        lines = []
        return create_msgs_from_lines(lines)

     

async def run(sensor_file, ws_address):
    async with websockets.connect(ws_address) as websocket:
        data = dict(topic="sensor:sensorB",
                    event="phx_join", payload={}, ref=1)
        # data is a dictionary containing necessary info for a join request to the topic.
        await websocket.send(json.dumps(data))

        print("Joined")

        while True:
            # waiting for retrieve_sensor_data function to return a value
            msgs = await retrieve_sensor_data2(sensor_file)
            # for msg in msgs:
                # sending the message to the phoenix channel
            await websocket.send(json.dumps(msgs[0]))
            # constantly receiving data from the channel
            call = await websocket.recv()
            # converting to json
            control = json.loads(call)
            print(control)
            time.sleep(0.5)


def cmd_line_arguments():
    parser = argparse.ArgumentParser(
        description='Read SpO2 sensor data and send to webapp')
    parser.add_argument('file',
                        help='The path to the file with sensor data csv (red,ir)')
    parser.add_argument('ws',
                        help='The address of the webapp websocket')

    return parser.parse_args()


if __name__ == '__main__':
    args = cmd_line_arguments()
    asyncio.get_event_loop().run_until_complete(run(args.file, args.ws))
    asyncio.get_event_loop().run_forever()
