import pyaudio  #録音機能を使うためのライブラリ
import wave     #wavファイルを扱うためのライブラリ
from google.cloud.speech import types
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types 
import io
import os

RECORD_SECONDS = 5 #録音する時間の長さ（秒）
WAVE_OUTPUT_FILENAME = "resources/sample.wav" #音声を保存するファイル名
iDeviceIndex = 0 #録音デバイスのインデックス番号
 
#基本情報の設定
FORMAT = pyaudio.paInt16 #音声のフォーマット
CHANNELS = 1   #モノラル
RATE = 16000            #サンプルレート
CHUNK = 2**11            #データ点数
# 翻訳言語
LANGUAGE = "ja-JP"

#フレーズセット
SPEECH_CONTEXTS = [{"phrases": "墨出し"},{"phrases": "ねこ持ってきて"},{"phrases": "ねこある"}]

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

    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        speech_contexts=speech_contexts,
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code=language)

    response = client.recognize(config, audio)
    for result in response.results:
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        os.remove(WAVE_OUTPUT_FILENAME)
    
if __name__ == '__main__':
    recording()
    transcribe_file(WAVE_OUTPUT_FILENAME, LANGUAGE)