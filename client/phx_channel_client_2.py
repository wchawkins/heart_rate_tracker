import argparse
import asyncio
import csv
import websockets
import json
import time


def line_to_msg(line):
    col = line.split(',')
    sample = {"red": col[0], "ir": col[1]}
    msg = {"topic": "sensor:sensorB", "event": "new_data",
           "payload": {"sample": sample}, "ref": None}
    return msg


def create_msgs_from_lines(lines):
    return [line_to_msg(line) for line in lines]


async def run(sensor_file, ws_address):
    async with websockets.connect(ws_address) as websocket:
        data = dict(topic="sensor:sensorB",
                    event="phx_join", payload={}, ref=1)
        # data is a dictionary containing necessary info for a join request to the topic.
        await websocket.send(json.dumps(data))

        print("Joined")

        with open(sensor_file, newline='') as file:
            for line in file:
                print(line)
                msg = line_to_msg(line)
                await websocket.send(json.dumps(msg))


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
    # asyncio.get_event_loop().run_forever()
