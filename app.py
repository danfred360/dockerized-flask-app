from flask import Flask, render_template
import os
import platform
import socket
import re
import uuid
import json
import psutil
import logging
import datetime
import json
import hashlib

def get_system_info():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / 1024.0 **3)) + " GB"
        # response = json.dumps(info)
    except Exception as e:
        logging.exception(e)
    return info

app = Flask(__name__)

context = {}
context['system_info'] = get_system_info()

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html', context=context)

@app.route("/home/", methods=['GET'])
def home():
    return index()

@app.route("/dashboard/", methods=['GET'])
def dashboard():
    return render_template('dashboard.html', context=context)

@app.route("/system_info/", methods=['GET'])
def system_info():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / 1024.0 **3)) + " GB"
        response = json.dumps(info)
    except Exception as e:
        logging.exception(e)
    return response, 200

# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(debug=True, host='0.0.0.0', port=port)