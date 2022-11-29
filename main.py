from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

import translate as func1
import detect as func2

import boto3

import message as m #メッセージクラス呼び出し

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    actives = [False, False, False]
    return render_template('index.html', actives=actives)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    actives = [True, False, False]
    langs = ['', '']
    messages = []

    if request.method == 'POST':
        #翻訳元テキスト
        source = request.form.get('sourceTxt')
        #翻訳先テキスト、音声パス
        result, audio_path, error = func1.translate(source, request.form.get('lang1'), request.form.get('lang2'))

        langs = [request.form.get('lang1'), request.form.get('lang2')]

        #メッセージ
        if error:
            #対応できない言語で翻訳しようとした場合（例：ラテン語）
            messages = [m.Message("alert alert-danger", "対応できない言語なので、翻訳に失敗しました。")]
        else:
            #翻訳に成功した場合
            messages = [m.Message("alert alert-success", "翻訳に成功しました。")]
    else:
        source = ''
        result = ''
        audio_path = ''
    
    return render_template('translate.html', actives=actives, langs=langs, messages=messages, source=source, result=result, audio_path=audio_path)

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
        target = 'もの'
        if t == 2:
            target = '文字列'

        result_url, result_str, count = func2.detect_any(t)

        #メッセージ
        if count > 0:
            #認識に成功した場合
            messages = [m.Message("alert alert-success", "認識に成功しました。")]
        else:
            #一つも認識されなかった場合
            messages = [m.Message("alert alert-warning", "一つも認識されていないようです。")]
    else:
        #GETされたとき
        result_url = ''
        result_str = []

        messages = []
        target = ''
    
    return render_template('rekognition.html', actives=actives, messages=messages, target=target, result=result_url, result_str=result_str)

@app.route('/emotion', methods=['GET', 'POST'])
def emotion():
    actives = [False, False, True]

    sent_text = ''
    results = []
    messages = []

    if request.method == 'POST':
        try:
            sent_text = request.form.get('txt')

            #日本語には対応できないので、英語に翻訳しておく。
            translate = boto3.client('translate')
            eng = translate.translate_text(
                Text=sent_text, SourceLanguageCode='auto', TargetLanguageCode='en'
            )['TranslatedText']

            #感情解析
            comprehend = boto3.client('comprehend')
            emotions = comprehend.detect_sentiment(Text=eng, LanguageCode='en')

            #感情ごとのスコアを配列にまとめる。
            results = [
                emotions["SentimentScore"]["Positive"],
                emotions["SentimentScore"]["Negative"],
                emotions["SentimentScore"]["Neutral"],
                emotions["SentimentScore"]["Mixed"],
                emotions["Sentiment"]
            ]

            #解析に成功した場合のメッセージ
            messages = [m.Message("alert alert-success", "解析に成功しました。")]
        except:
            sent_text = ''
            results = []

            #エラーが発生した場合のメッセージ
            messages = [m.Message("alert alert-danger", "解析に失敗しました。")]

    return render_template('emotion.html', actives=actives, messages=messages, sent_text=sent_text, results=results)

if __name__ == '__main__':
    app.run(debug=True)