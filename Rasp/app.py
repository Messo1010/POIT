from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect    
import time
import random
import math
import serial
import matplotlib.pyplot as plt
import numpy as np

async_mode = None

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

ser = serial.Serial("/dev/ttyS1", 9600)
ser.buaudrate = 9600

def background_thread(args):
    start_clock = time.time()
    count = 0
    A = 1
    while True:
        if args:
            A = dict(args).get('A')
        if type(A) == str:
            A = A.encode('utf-8')
            Ts = float(A)
        else:
            #kod na rozdelenie retazca
            read_serial = ser.readline()
            retazec = str(read_serial[0:len(read_serial)].decode("utf-8"))
            list_values = retazec.split(',')[0]#ciarka ako identifikator rozdelenia
            list_values_1 = retazec.split(',')[1]#cislo hran. zatv. je poradie hodnoty
            list_values_2 = retazec.split(',')[2]
    
        clock = time.time() - start_clock
        start = dict(args).get('start')
        print (read_serial)
        print (start)
        print (args)
        print (type(A))
        socketio.sleep(0.1)
        count += 1
        
        if start:    
            socketio.emit('my_response',
                          {'data': int(list_values),'data1': int(list_values_1),'data2': int(list_values_2), 'count': clock},
                          namespace='/test')

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('my_event', namespace='/test')
def test_message(message):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['A'] = message['value']    
    emit('my_response',
         {'data': message['value'],'data1': message['value'],'data2': message['value'], 'count': session['receive_count']})
    
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('start_request', namespace='/test')
def start_request():
    session['start'] = 1
    print (session['start'])
         
@socketio.on('stop_request', namespace='/test')
def stop_request():
    session['start'] = 0
    print (session['start'])

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    emit('my_response', {'data': 'Connected', 'count': 0})
  

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)