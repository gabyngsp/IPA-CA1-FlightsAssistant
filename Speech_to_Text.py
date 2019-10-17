# Load library into computer memory:
import io
from google.cloud import speech


client_speech2text = speech.SpeechClient.from_service_account_json(
        "D:\Software-Agent\Intelligent-Process-Automation\workshop_blog-master\wechat_tool_py3_local\iss-ipa-e084b16a39bf.json")


parm_runtime_env_GCP = False

import subprocess


# Running Speech API
def didi_mp3_audio_conversion(audio_file_input, audio_type='flac'):
    audio_file_output = str(audio_file_input) + '.' + str(audio_type)

    if parm_runtime_env_GCP:  # using Datalab in Google Cloud Platform
        # GCP: use avconv to convert audio
        retcode = subprocess.call(['avconv', '-i', audio_file_input, '-ac', '1', audio_file_output])
    else:  # using an iss-vm Virtual Machine, or local machine
        # VM : use ffmpeg to convert audio
        retcode = subprocess.call(['ffmpeg', '-i', audio_file_input, '-ac', '1', audio_file_output])

    if retcode == 0:
        print('[  O K  ] Converted  audio file for API: %s' % audio_file_output)
    else:
        print('[ ERROR ] Function: didi_mp3_audio_conversion() Return Code is : {}'.format(retcode))

    return audio_file_output  # return file name string only


# API control parameter for  'voice to text' language
parm_speech_recognition_language = 'en-US'


def didi_speech2text(speech_file, didi_language_code='en-US'):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(language_code=didi_language_code)

    response = client_speech2text.recognize(config, audio)
    print('response : ', response)

    for result in response.results:
        print(u'Transcript : {}'.format(result.alternatives[0].transcript))
        print(u'Confidence : {0:.3f}'.format(result.alternatives[0].confidence))

    return response

response = didi_speech2text(didi_mp3_audio_conversion('191016-122903.mp3'), parm_speech_recognition_language)