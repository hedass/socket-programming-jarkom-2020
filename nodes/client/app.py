from json.decoder import JSONDecodeError
from flask import Flask, render_template, request, jsonify
from json import dumps, loads
from ast import literal_eval

import utils
import socket

app = Flask(__name__)
app.debug = True


def send_code(code, lang):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)
        utils.send_data(s, f"{lang}{code}", utils.Request.EXECUTE_JOB.value)
        job_id = utils.receive_data(s)

    return job_id


def _status():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)


def _available():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)
        utils.send_flag(s, utils.Request(1).value)
        output = utils.receive_data(s)
        avail = utils.WorkerStatus(int(output)).name
        return avail


def _get_output(job_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)
        utils.send_data(s, job_id, utils.Request(5).value)
        output = utils.receive_data(s)
        try:
            loads(output)
        except JSONDecodeError as e:
            output = {
                'message': output
            }
            return output
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
        job_id = send_code(code, language)
        json_output = {'job_id': job_id}
        return jsonify(json_output)
    return render_template('index.html')


@app.route('/availability')
def get_availability():
    return render_template('node_availability.html')


@app.route('/output/<job_id>')
def get_html_output(job_id):
    return render_template('output.html', job_id=job_id)


@app.route('/output/<job_id>.json')
def get_output(job_id):
    output = _get_output(job_id)
    return jsonify(output)


@app.route('/availability.json', methods=['GET'])
def available():
    output = _available()
    json_output = {'STATUS': output}
    return jsonify(json_output)


@app.route('/status', methods=['GET'])
def status():
    output = _status()
    return jsonify(output)
