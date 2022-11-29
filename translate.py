import boto3, contextlib

languages = {
    'auto' : '自動',
    'ar' : 'アラビア語', 
    'cs' : 'チェコ語',
    'da' : 'デンマーク語',
    'en' : '英語',
    'es' : 'スペイン語',
    'fi' : 'フィンランド語',
    'fr' : 'フランス語',
    'de' : 'ドイツ語',
    'he' : 'ヘブライ語',
    'id' : 'インドネシア語',
    'it' : 'イタリア語',
    'ja' : '日本語',
    'ko' : '韓国語',
    'nl' : 'オランダ語',
    'pl' : 'ポーランド語',
    'pt' : 'ポルトガル語',
    'ru' : 'ロシア語',
    'sv' : 'スウェーデン語',
    'tr' : 'トルコ語',
    'zh' : '中国語（簡体字）',
    'zh-TW' : '中国語（繁体字）'
}
# voice_id_dict = {
#     "ar" : "Zeina",
#     "da" : "Naja",
#     "en" : "Joanna",
#     "es" : "Lucia",
#     "fr" : "Ceilne",
#     "de" : "Marlene",
#     "it" : "Carla",
#     "ja" : "Mizuki",
#     "ko" : "Seoyeon",
#     "nl" : "Lotte",
#     "pl" : "Ewa",
#     "pt" : "Vitoria",
#     "ru" : "Tatyana",
#     "sv" : "Astrid",
#     "tr" : "Filiz",
#     "zh" : "Zhiyu",
#     "zh-TW" : "Zhiyu"
# }

#======= 翻訳 =======
def translate(sequence, lang1, lang2):
    try:
        #Translateサービスクライアントを作成
        translate = boto3.client('translate')
        #翻訳元言語から翻訳先言語に翻訳
        result = translate.translate_text(
            Text=sequence, SourceLanguageCode=lang1, TargetLanguageCode=lang2
        )['TranslatedText']

        # #音声合成
        # if lang2 in voice_id_dict:
        #     polly = boto3.client('polly')
        #     read_text = polly.synthesize_speech(
        #         Text=result, OutputFormat='mp3', VoiceId=voice_id_dict[lang2]
        #     )
        #     #音声ファイルの保存
        #     path = 'static/audio/read_text.mp3'
        #     with contextlib.closing(read_text['AudioStream']) as stream:
        #         with open(path, 'wb') as file:
        #             file.write(stream.read())
        # else:
        #     path = ''
        path = ''
        
        #翻訳メモ
        """
        例）
        日本語
        こんにちは

        英語
        Hi
        """
        with open('static/memo/translate_out.txt', 'w', encoding='utf-8') as file_out:
            file_out.write(languages[lang1] + '\n')
            file_out.write(sequence + '\n\n')
            file_out.write(languages[lang2] + '\n')
            file_out.write(result)
        
        #翻訳後の文章を返す
        return result, path
    except:
        print("Error!")
        return '', ''