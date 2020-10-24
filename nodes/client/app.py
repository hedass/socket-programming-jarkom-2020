from flask import Flask, render_template, request, jsonify
from utils import EXEC_FLAG, MASTER_SOCK, TOKEN, EOF, LANGUAGE

import io
import socket

app = Flask(__name__)
app.debug = True

def kirim_master(code, lang):
    data = io.BytesIO((str(lang) + code).encode())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(MASTER_SOCK)
        s.send((TOKEN + EXEC_FLAG).encode())
        while 1:
            chunk = data.read(1024)
            if not chunk:
                break
            s.send(chunk)
        s.send(EOF.encode())
        output = ''
        while 1:
            reply = s.recv(1024).decode()
            if not reply:
                break
            output += reply

    return output

def _cancel():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(MASTER_SOCK)
        s.send(1)

        output = s.recv(1024).decode()
        return output

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('code').replace('\r\n', '\n')
        language = request.form.get('language')
        if (language not in LANGUAGE):
            return render_template('index.html', code=code, language=language)
        language = LANGUAGE[language]
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
