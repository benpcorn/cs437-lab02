import socket
import time
import datetime
import json
from flask import Flask, jsonify
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

@app.route('/api/')
def index():
    return get_stats()

@app.route('/api/v1/stop', methods=['POST'])
def stop():
    print('Stop')
    motor.setMotorModel(0,0,0,0)
    return get_stats()

@app.route('/api/v1/forward', methods=['POST'])
def forward():
    print('Forward')
    motor.setMotorModel(-1000,-1000,-1000,-1000)
    time.sleep(.1)
    stop()
    return get_stats()

@app.route('/api/v1/backward', methods=['POST'])
def backward():
    print('Backward')
    motor.setMotorModel(1000,1000,1000,1000)
    time.sleep(.1)
    stop()
    return get_stats()

@app.route('/api/v1/left', methods=['POST'])
def left():
    print('Turn left')
    motor.setMotorModel(500,500,-2000,-2000)
    time.sleep(.1)
    stop()
    return get_stats()

@app.route('/api/v1/right', methods=['POST'])
def right():
    print('Turn right')
    motor.setMotorModel(-2000,-2000,500,500)
    time.sleep(.1)
    stop()
    return get_stats()

@app.route('/api/v1/stats', methods=['GET'])
def get_stats():
    # [battery, us_distance, traveled_dist, moving_direction]
    stats = [5, 10, 15, 20]
    return jsonify(stats)

app.run()