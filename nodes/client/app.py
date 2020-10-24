from flask import Flask, render_template, request, jsonify
from utils import EXECUTOR_SOCK, CANCEL_SOCK

import io
import socket

app = Flask(__name__)
app.debug = True

def kirim_master(code, lang):
    data = io.BytesIO(code)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(EXECUTOR_SOCK)
        while 1:
            chunk = data.read(1024)
            if not chunk:
                break
            s.send(chunk)
        s.shutdown(socket.SHUT_WR)
        output = ''
        while 1:
            reply = s.recv(1024)
            if not reply:
                break
            output += reply

    return output

def _cancel():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(CANCEL_SOCK)
        s.send(1)
        s.shutdown(socket.SHUT_WR)

        output = s.recv(1024).decode()
        return output

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('code').replace('\r\n', '\n')
        language = request.form.get('language')
        output = kirim_master(code, language)
        context = {
            'code': code,
            'output': output,
            'language': language
        }
        return render_template('index.html', **context)
    return render_template('index.html')

@app.route('/cancel', methods=['POST'])
def cancel():
    output = _cancel()
    json_dict = {'cancel': 1}
    return jsonify(json_dict)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000)
