import boto3
from PIL import Image, ImageFont, ImageDraw
from werkzeug.utils import secure_filename

#======= 翻訳 =======
def translate(sequence, lang1, lang2):
    #Translateサービスクライアントを作成
    translate = boto3.client('translate')
    #翻訳元言語から翻訳先言語に翻訳
    result = translate.translate_text(
        Text=sequence, SourceLanguageCode=lang1, TargetLanguageCode=lang2)
    #翻訳後の文章を返す
    return result['TranslatedText']

#======= 画像認識 =======
def detect_any(filename, t):
    #Translate、Rekognitionサービスクライアントを作成
    translate = boto3.client('translate')
    rekognition = boto3.client('rekognition')
    #画像ファイルを開く
    with open("static/image/" + filename, 'rb') as file:
        if t == 2:
            #画像内の文字列を検出
            result = rekognition.detect_text(Image={'Bytes': file.read()})
        else:
            #画像内の物および人物を検出
            result = rekognition.detect_labels(Image={'Bytes': file.read()})
    #入力画像のファイルを読み込む
    image_in = Image.open("static/image/" + filename)
    #画像のサイズを取得
    w, h = image_in.size
    #出力画像の初期化
    image_draw = ImageDraw.Draw(image_in)

    #検出された物のリスト
    detected_list = []
    #人物のリスト（物を検出するときに対象外となるもの）
    people_list = [
        'Person',
        'Baby', 'Child', 'Adult',
        'Boy', 'Girl',
        'Man', 'Woman',
        'Male', 'Female'
    ]

    if t == 2:
        #文字列の場合
        for text in result['TextDetections']:
            #バウンディングボックスを取得
            box = text['Geometry']['BoundingBox']
            #文字列の左、上、右、下の座標を計算
            left = int(box['Left'] * w)
            top = int(box['Top'] * h)
            right = left + int(box['Width'] * w)
            bottom = top + int(box['Height'] * h)
            #入力画像から出力画像に文字列の部分を貼り付け
            image_draw.rectangle([(left, top), (right, bottom)],
                outline=(255, 0, 0), width=2)
            
            #検出された文字列
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
        #物の場合
        for label in result['Labels']:
            if label['Instances'] and label['Name'] not in people_list:
                #英語名で検出されるため、日本語に翻訳する
                trans_name = translate.translate_text(
                    Text=label['Name'], SourceLanguageCode='en', TargetLanguageCode='ja'
                )['TranslatedText']

                for instance in label['Instances']:
                    #バウンディングボックスを取得
                    box = instance['BoundingBox']
                    #文字列の左、上、右、下の座標を計算
                    left = int(box['Left'] * w)
                    top = int(box['Top'] * h)
                    right = left + int(box['Width'] * w)
                    bottom = top + int(box['Height'] * h)
                    #出力画像に物の部分を赤枠で囲む
                    image_draw.rectangle([(left, top), (right, bottom)],
                        outline=(255, 0, 0), width=2)
                    
                    #物の名称
                    font = ImageFont.truetype("meiryo.ttc", 30)
                    position = (left, top - 35)
                    text = trans_name

                    bbox = image_draw.textbbox(position, text, font=font)
                    image_draw.rectangle(bbox, fill=(255, 0, 0))
                    image_draw.text(position, text, font=font, fill="black")
                detected_list.append(trans_name)
        # 出力画像をファイルに保存
        image_in.save('static/image/things_'+filename)
        return 'static/image/things_' + filename, detected_list
    else:
        #人物の場合
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
                    #出力画像に人物の部分を赤枠で囲む
                    image_draw.rectangle([(left, top), (right, bottom)],
                        outline=(255, 0, 0), width=2)
            
        # 出力画像をファイルに保存
        image_in.save('static/image/people_'+filename)
        return 'static/image/people_' + filename, detected_list