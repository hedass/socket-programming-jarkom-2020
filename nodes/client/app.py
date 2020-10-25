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
        utils.send_data(s, f"{lang}{code}", utils.EXEC_FLAG)
        output = utils.receive_data(s)
        output = literal_eval(output)
        output['stdout'] = output['stdout'].decode()
        output['stderr'] = output['stderr'].decode()
        output = dumps(output)

    return output


def _cancel():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)
        s.send(1)

        output = s.recv(1024).decode()
        return output


def _status():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)


def _available():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(utils.MASTER_SOCK)
        utils.send_flag(s, utils.GET_AVAIL)
        output = utils.receive_data(s)
        avail = utils.AVAILABILITY[int(output) - 1]
        return avail


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        code = data.get('code').replace('\r\n', '\n')
        language = data.get('language')
        if (language not in utils.LANGUAGE):
            return render_template('index.html', code=code, language=language)
        language = utils.LANGUAGE[language]
        output = kirim_master(code, language)
        context = {
            'code': code,
            'output': output,
            'language': language
        }
        return jsonify(context)
        # return render_template('index.html', **context)
    return render_template('index.html')


@app.route('/available', methods=['GET'])
def available():
    output = _available()
    return jsonify(output)


@app.route('/status', methods=['GET'])
def status():
    output = _status()
    return jsonify(output)


@app.route('/cancel', methods=['POST'])
def cancel():
    output = _cancel()
    json_dict = {'cancel': 1}
    return jsonify(json_dict)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000)
