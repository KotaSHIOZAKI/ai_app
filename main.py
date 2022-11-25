from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

import translate as func1
import detect as func2

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    actives = [False, False, False]
    return render_template('index.html', actives=actives)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    actives = [True, False, False]

    if request.method == 'POST':
        #翻訳元テキスト
        source = request.form.get('sourceTxt')
        #翻訳先テキスト、音声パス
        result, audio_path = func1.translate(source, request.form.get('lang1'), request.form.get('lang2'))
    else:
        source = ''
        result = ''
        audio_path = ''
    return render_template('translate.html', actives=actives, source=source, result=result, audio_path=audio_path)

@app.route('/image', methods=['GET', 'POST'])
def image():
    actives = [False, True, False]

    #画像認識ページ
    if request.method == 'POST':
        #POSTされたとき
        
        #ファイル名を取得
        f = request.files.get('image')
        #ファイルを保存するディレクトリを指定
        filepath = 'static/image/in.jpg'
        #ファイルを保存する
        f.save(filepath)

        #検出対象（０＝人物、１＝物、２＝文字列）
        t = int(request.form.get('type'))

        result_url, result_str = func2.detect_any(t)
    else:
        #GETされたとき
        result_url = ''
        result_str = []
    return render_template('rekognition.html', actives=actives, result=result_url, result_str=result_str)

@app.route('/emotion')
def emotion():
    actives = [False, False, True]
    return render_template('emotion.html', actives=actives)

if __name__ == '__main__':
    app.run(debug=True)