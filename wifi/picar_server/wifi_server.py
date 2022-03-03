import re
import socket
import time
import datetime
import json
from flask import Flask, jsonify, request
from sys import platform
from gpiozero import CPUTemperature
from Ultrasonic import *
from servo import *

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
cpu = CPUTemperature()
us = Ultrasonic()
servo = Servo()

# Init
last_angle_s0 = 90
last_angle_s1 = 90

def init_servos():
    servo.setServoPwm('0',90)
    servo.setServoPwm('1',90)
    global last_angle_s0
    global last_angle_s1
    last_angle_s1 = 90
    last_angle_s0 = 90

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
    try:
        return us.get_distance()
    except:
        0

def get_temperature():
    try:
        return cpu.temperature
    except:
        return 0

def get_servo1_angle():
    return last_angle_s1

def get_servo0_angle():
    return last_angle_s0

@app.route('/api/v1/vitals', methods=['GET'])
def get_stats():
    stats = {
        "us_dist": get_us_dist(), 
        "temp": get_temperature(), 
        "servo1_angle": get_servo1_angle(), 
        "servo0_angle": get_servo0_angle()
    }
    return jsonify(stats)

@app.route('/api/v1/servo', methods=['POST'])
def set_servo():
    response = {}
    request_data = request.get_json()

    global last_angle_s0
    global last_angle_s1

    if request_data is None or ('angle' not in request_data and 'servo' not in request_data):
        return {"code": 400, "message": "servo and angle must be provided in request."} 

    servo_id = request_data['servo']
    angle = int(request_data['angle'])

    if servo_id == 1:
        servo.setServoPwm('1', angle)
        last_angle_s1 = angle
    elif servo_id == 0:
        servo.setServoPwm('0', angle)
        last_angle_s0 = angle

    return {"code": 200, "message": "Servo angle set"}

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

# Run
app.run(debug=True, port=5000, host='0.0.0.0')
init_servos()