from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        code = request.form.get('code').replace('\r\n', '\n')
        language = request.form.get('language')

        print(code.encode())
        print(language)

    return render_template('index.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000)
