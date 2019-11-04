#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""
# from google.cloud import speech_v1p1beta1
# from google.cloud.speech_v1p1beta1 import enums
import argparse

# 翻訳言語
LANGUAGE = "ja-JP"
# ファイルのサンプルレート
SAMPLE_RATE =16000

#フレーズセット
SPEECH_CONTEXTS = [{"phrases": "積算して"},{"phrases": "墨出し"}]

# [START speech_transcribe_sync]
def transcribe_file(speech_file, language, sample_rate = SAMPLE_RATE, speech_contexts = SPEECH_CONTEXTS):
    """Transcribe the given audio file."""
    from google.cloud.speech import types
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types 
    import io

    client = speech.SpeechClient()

    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        speech_contexts=speech_contexts,
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code=language)
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    response = client.recognize(config, audio)
    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
    # [END speech_python_migration_sync_response]
# [END speech_transcribe_sync]
    # encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    # config = {
    #     "speech_contexts": speech_contexts,
    #     "sample_rate_hertz": sample_rate,
    #     "language_code": language,
    #     "encoding": encoding,
    # }
    # # open audio file
    # with io.open(speech_file, 'rb') as audio_file:
    #     content = audio_file.read()
    
    # audio = speech_v1p1beta1.types.RecognitionAudio(content=content)
    
    # response = client.recognize(config, audio)
    # for result in response.results:
    #     # First alternative is the most probable result
    #     alternative = result.alternatives[0]
    #     print(u"Transcript: {}".format(alternative.transcript))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    transcribe_file(args.path, LANGUAGE)
