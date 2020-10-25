from flask import Flask, render_template, request, jsonify
from flask import json
from ast import literal_eval
from json import dumps

import utils
import socket

app = Flask(__name__)
app.debug = True


def kirim_master(code, lang):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)
        utils.send_data(s, f"{lang}{code}", utils.Request.EXECUTE_JOB)
        job_id = utils.receive_data(s)

    return job_id


def _cancel(job_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)
        utils.send_data(s, job_id, utils.Request(4))

        output = utils.receive_data(s)
        return output


def _status():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)


def _available():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)
        utils.send_flag(s, utils.Request(1))
        output = utils.receive_data(s)
        avail = utils.WorkerStatus(int(output)).name
        return avail


def _get_output(job_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)
        utils.send_data(s, job_id, utils.Request(5))
        output = utils.receive_data(s)
        print(output)
        try:
            int(output)
            return output
        except ValueError as e:
            pass
        output = literal_eval(output)
        output['stdout'] = output['stdout'].decode()
        output['stderr'] = output['stderr'].decode()
        output = dumps(output)
        return output


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        code = data.get('code').replace('\r\n', '\n')
        language = data.get('language')
        if (language not in utils.LanguageCode.list()):
            return jsonify({'error': 'Language unsupported'})
        language = utils.LanguageCode.list().index(language) + 1
        job_id = kirim_master(code, language)
        json_output = {'job_id': job_id}
        return jsonify(json_output)
    return render_template('index.html')


@app.route('/output/<job_id>')
def get_output(job_id):
    output = _get_output(job_id)
    return jsonify(output)


@app.route('/available', methods=['GET'])
def available():
    output = _available()
    json_output = {'STATUS': output}
    return jsonify(json_output)


@app.route('/status', methods=['GET'])
def status():
    output = _status()
    return jsonify(output)


@app.route('/cancel/<job_id>', methods=['POST'])
def cancel(job_id):
    output = _cancel(job_id)
    json_dict = {'message': output}
    return jsonify(json_dict)
