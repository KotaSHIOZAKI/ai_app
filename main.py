from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

import functions as func

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        f = request.files.get('image')
        #ファイル名を取得
        filename = secure_filename(f.filename)
        #ファイルを保存するディレクトリを指定
        filepath = 'static/image/' + filename
        #ファイルを保存する
        f.save(filepath)

        t = int(request.form.get('type'))

        result_url, result_str = func.detect_text(filename, t)
    else:
        result_url = ''
        result_str = []
    return render_template('rekognition.html', result=result_url, result_str=result_str)

if __name__ == '__main__':
    app.run(debug=True)