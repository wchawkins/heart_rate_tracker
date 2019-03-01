from websocket import create_connection
import json
import sys

def send_data(ws, username, spo2, hr, temp):
    msg = {"topic": "sensor:" + username, "event": "new_data",
           "payload": {"spo2": spo2, "hr": hr, "temp": temp}, "ref": None}
    ws.send(json.dumps(msg))

def join(address, username):
    """ `address` should look like "ws://host:port" for non-SSL
    and "wss://host:port" for a SSL server """

    address = address + '/socket/websocket'
    ws = create_connection(address)
    join = { "topic": "sensor:" + username, "event": "phx_join", "payload": {},
            "ref": 1 }
    ws.send(json.dumps(join))
    print ws.recv()
    return ws

if __name__ == "__main__":
    # `address` should be the hostname and port of the web app
    # e.g. "192.168.0.156:4000"
    address = sys.argv[1]

    # `username` should be the username of the one this sensor data belongs to
    username = sys.argv[2]

    ws = join(address, username)
    send_data(ws, username, 98, 64, 32)
    send_data(ws, username, 95, 60, 31)
    ws.close()
