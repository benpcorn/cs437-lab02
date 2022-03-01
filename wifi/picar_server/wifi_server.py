import socket
import time
import datetime
import json
from flask import Flask, jsonify, request
from sys import platform

if platform == "linux" or platform == "linux2":
    from Motor import *
else:
    class Motor:
        def __init__(self):
            self.data = []
        
        def setMotorModel(self,a,b,c,d):
            return


app = Flask(__name__)
app.config["DEBUG"] = True

last_send = ''

motor = Motor()

HOST = "192.168.3.49" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

def stop():
    print('Stop')
    motor.setMotorModel(0,0,0,0)

def forward():
    print('Forward')
    motor.setMotorModel(-1000,-1000,-1000,-1000)
    time.sleep(.1)
    stop()

def backward():
    print('Backward')
    motor.setMotorModel(1000,1000,1000,1000)
    time.sleep(.1)
    stop()

def left():
    print('Turn left')
    motor.setMotorModel(500,500,-2000,-2000)
    time.sleep(.1)
    stop()

def right():
    print('Turn right')
    motor.setMotorModel(-2000,-2000,500,500)
    time.sleep(.1)
    stop()

def get_us_dist():
    return 5

def get_temperature():
    return 33.5

def get_heading():
    return 'N'

def get_last_direction():
    return 'Left'

@app.route('/api/v1/vitals', methods=['GET'])
def get_stats():
    stats = {
        "us_dist": get_us_dist(), 
        "temp": get_temperature(), 
        "heading": get_heading(), 
        "direction": get_last_direction()
    }
    return jsonify(stats)

@app.route('/api/v1/move', methods=['POST'])
def move():
    response = {}
    request_data = request.get_json()

    if request_data is None or 'direction' not in request_data:
        return {"code": 400, "message": "Direction not provided."} 

    direction = request_data['direction']

    if direction == "left":
        left()
        response = {"code": 200, "message": "Turning left"}
    elif direction == "right":
        right()
        response = {"code": 200, "message": "Turning right"}
    elif direction == "forward":
        forward()
        response = {"code": 200, "message": "Moving forward"}
    elif direction == "backward":
        backward()
        response = {"code": 200, "message": "Moving backward"}
    elif direction == "stop":
        stop()
        response = {"code": 200, "message": "Stopping"}
    else:
        stop()
        response = {"code": 400, "message": "Unknown direction. Stopping car."}

    return jsonify(response)

#Run
app.run()