from flask import Flask, render_template, request
import boto3
from PIL import Image, ImageFont, ImageDraw
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files.get('image')
        #ファイル名を取得
        filename = secure_filename(f.filename)
        #ファイルを保存するディレクトリを指定
        filepath = 'static/image/' + filename
        #ファイルを保存する
        f.save(filepath)

        t = int(request.form.get('type'))

        result_url, result_str = detect_text(filename, t)
    else:
        result_url = ''
        result_str = []
    return render_template('index.html', result=result_url, result_str=result_str)

def detect_text(filename, t):
    #Rekognitionサービスクライアントを作成
    translate = boto3.client('translate')
    rekognition = boto3.client('rekognition')
    #画像ファイルを開く
    with open("static/image/" + filename, 'rb') as file:
        #(1)画像内の文字列を検出
        if t == 2:
            result = rekognition.detect_text(Image={'Bytes': file.read()})
        else:
            result = rekognition.detect_labels(Image={'Bytes': file.read()})
    #入力画像のファイルを読み込む
    image_in = Image.open("static/image/" + filename)
    #画像のサイズを取得
    w, h = image_in.size

    image_draw = ImageDraw.Draw(image_in)

    detected_list = []

    people_list = [
        'Person',
        'Baby', 'Child', 'Adult',
        'Boy', 'Girl',
        'Man', 'Woman',
        'Male', 'Female'
    ]

    if t == 2:
        for text in result['TextDetections']:
            #(3)バウンディングボックスを取得
            box = text['Geometry']['BoundingBox']
            #文字列の左、上、右、下の座標を計算
            left = int(box['Left'] * w)
            top = int(box['Top'] * h)
            right = left + int(box['Width'] * w)
            bottom = top + int(box['Height'] * h)
            #(4)入力画像から出力画像に文字列の部分を貼り付け
            image_draw.rectangle([(left, top), (right, bottom)],
                outline=(255, 0, 0), width=2)
            
            font = ImageFont.truetype("segoeui.ttf", 30)
            position = (left, top - 35)
            tx = text['DetectedText']

            bbox = image_draw.textbbox(position, tx, font=font)
            image_draw.rectangle(bbox, fill=(255, 0, 0))
            image_draw.text(position, tx, font=font, fill="black")

            if text['DetectedText'] not in detected_list:
                detected_list.append(text['DetectedText'])
            
        # 出力画像をファイルに保存
        image_in.save('static/image/texts_'+filename)
        return 'static/image/texts_' + filename, detected_list
    elif t == 1:
        for label in result['Labels']:
            if label['Instances'] and label['Name'] not in people_list:
                trans_name = translate.translate_text(
                    Text=label['Name'], SourceLanguageCode='en', TargetLanguageCode='ja'
                )['TranslatedText']

                for instance in label['Instances']:
                    #(3)バウンディングボックスを取得
                    box = instance['BoundingBox']
                    #文字列の左、上、右、下の座標を計算
                    left = int(box['Left'] * w)
                    top = int(box['Top'] * h)
                    right = left + int(box['Width'] * w)
                    bottom = top + int(box['Height'] * h)
                    #(4)入力画像から出力画像に文字列の部分を貼り付け
                    image_draw.rectangle([(left, top), (right, bottom)],
                        outline=(255, 0, 0), width=2)
                    
                    font = ImageFont.truetype("meiryo.ttc", 30)
                    position = (left, top - 35)
                    text = trans_name

                    bbox = image_draw.textbbox(position, text, font=font)
                    image_draw.rectangle(bbox, fill=(255, 0, 0))
                    image_draw.text(position, text, font=font, fill="black")
                detected_list.append(trans_name + '(' + label['Name'] + ')')
        # 出力画像をファイルに保存
        image_in.save('static/image/things_'+filename)
        return 'static/image/things_' + filename, detected_list
    else:
        for label in result['Labels']:
            if label['Instances'] and label['Name'] == 'Person':
                for instance in label['Instances']:
                    #(3)バウンディングボックスを取得
                    box = instance['BoundingBox']
                    #文字列の左、上、右、下の座標を計算
                    left = int(box['Left'] * w)
                    top = int(box['Top'] * h)
                    right = left + int(box['Width'] * w)
                    bottom = top + int(box['Height'] * h)
                    #(4)入力画像から出力画像に文字列の部分を貼り付け
                    image_draw.rectangle([(left, top), (right, bottom)],
                        outline=(255, 0, 0), width=2)
            
        # 出力画像をファイルに保存
        image_in.save('static/image/people_'+filename)
        return 'static/image/people_' + filename, detected_list


if __name__ == '__main__':
    app.run(debug=True)