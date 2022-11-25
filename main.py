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
    #画像認識ページ
    if request.method == 'POST':
        #POSTされたとき
        
        #ファイル名を取得
        f = request.files.get('image')
        filename = secure_filename(f.filename)
        #ファイルを保存するディレクトリを指定
        filepath = 'static/image/' + filename
        #ファイルを保存する
        f.save(filepath)

        #検出対象（０＝人物、１＝物、２＝文字列）
        t = int(request.form.get('type'))

        result_url, result_str = func.detect_any(filename, t)
    else:
        #GETされたとき
        result_url = ''
        result_str = []
    return render_template('rekognition.html', result=result_url, result_str=result_str)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        source = request.form.get('sourceTxt')
        result = func.translate(source, request.form.get('lang1'), request.form.get('lang2'))
    else:
        source = ''
        result = ''
    return render_template('translate.html', source=source, result=result)

if __name__ == '__main__':
    app.run(debug=True)