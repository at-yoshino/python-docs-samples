import pyaudio  #録音機能を使うためのライブラリ
import wave     #wavファイルを扱うためのライブラリ
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
import argparse
import io
import os

RECORD_SECONDS = 5 #録音する時間の長さ（秒）
WAVE_OUTPUT_FILENAME = "resources/sample.wav" #音声を保存するファイル名
iDeviceIndex = 0 #録音デバイスのインデックス番号
 
#基本情報の設定
FORMAT = pyaudio.paInt16 #音声のフォーマット
CHANNELS = 1             #モノラル
RATE = 44100            #サンプルレート
CHUNK = 2**11            #データ点数
# 翻訳言語
LANGUAGE = "ja-JP"

#フレーズセット
# ねこ：一輪車, ピッチ何台：コンクリート乗っけたトラック, 面（ツラ）→　読み方を指定できない...、表面。コンクリートの面とか？, 舟→
SPEECH_CONTEXTS = [{"phrases": "ねこ持ってきて","boost": 10.0},{"phrases": "ねこある", "boost": 10.0},{"phrases": "猫", "boost": 10.0}]
# {"phrases": "面どう", "boost": 10.0},
# {"phrases": "トラ張って","boost": 10.0}]
# ,{"phrases": "舟", "bppst":10.0},
# {"phrases": "スランプ試験OK"},{"phrases":"ピッチ何台"},{:"生コン柔らかくしください"},{"phrases":"コンクリート天端どう"},{"phrases":"面"}]

# Recording
def recording():
    audio = pyaudio.PyAudio() #pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        input_device_index = iDeviceIndex, #録音デバイスのインデックス番号
        frames_per_buffer=CHUNK)

    #--------------録音開始---------------
    print ("recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)


    print ("finished recording")
    #--------------録音終了---------------

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

# SpeechToText
def transcribe_file(speech_file, language, sample_rate = RATE, speech_contexts = SPEECH_CONTEXTS):
    """Transcribe the given audio file."""

    client = speech_v1p1beta1.SpeechClient()

    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "speech_contexts": speech_contexts,
        "sample_rate_hertz": sample_rate,
        "language_code": language,
        "encoding": encoding,
    }
    # open audio file
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
    
    audio = speech_v1p1beta1.types.RecognitionAudio(content=content)
    
    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
        os.remove(WAVE_OUTPUT_FILENAME)

if __name__ == '__main__':
    recording()
    transcribe_file(WAVE_OUTPUT_FILENAME, LANGUAGE)