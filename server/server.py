#!/usr/bin/env python3

import atexit
from flask import Flask, render_template, Blueprint, jsonify
from flask_socketio import send, emit
from flask_socketio import SocketIO

import threading
import time


SEND_INTERVAL = 1


class MessageSender(threading.Thread):
    def __init__(self):
        super(MessageSender, self).__init__()
        self._terminate = threading.Event()
        self._should_send_messages = threading.Event()
        self._counter = 0

    def start_streaming(self):
        self._should_send_messages.set()

    def stop_streaming(self):
        self._should_send_messages.clear()

    def terminate(self):
        self._terminate.set()

    def run(self):
        while not self._terminate.is_set():
            while (self._should_send_messages.is_set() and 
                   not self._terminate.is_set()):
                message = 'count: {}'.format(self._counter)
                print("sending message: {}".format(message))
                socketio.send(message, namespace="/test")
                self._counter += 1
                time.sleep(SEND_INTERVAL)
            time.sleep(SEND_INTERVAL)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

message_sender = MessageSender()
main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2', async_mode=socketio.async_mode)

@main_blueprint.route('/start_streaming', methods=['POST'])
def start_streaming():
    message_sender.start_streaming()
    return jsonify({'success': True})

@main_blueprint.route('/stop_streaming', methods=['POST'])
def stop_streaming():
    message_sender.stop_streaming()
    return jsonify({'success': True})

@socketio.on('message')
def handle_message(message, namespace='/test'):
    print('received message: ' + message)

@socketio.on('json')
def handle_json(json, namespace='/test'):
    print('received json: ' + str(json))

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    return json

if __name__ == '__main__':
    app.register_blueprint(main_blueprint)

    print("starting thread...")

    message_sender.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    #app.run(host='0.0.0.0', debug=True)

    message_sender.terminate()
    message_sender.join()

    print("exiting...")


