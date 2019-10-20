import io
import os
from google.cloud import speech
import subprocess
import spacy
from datetime import datetime as dt


#Instantiates a client - using 'service account json' file
client_speech2text = speech.SpeechClient.from_service_account_json(
        "D:\Software-Agent\Intelligent-Process-Automation\workshop_blog-master\wechat_tool_py3_local\iss-ipa-e084b16a39bf.json")


# Uncomment to run the code in local machine
parm_runtime_env_GCP = False


# Running Speech API
def audio_conversion(audio_file_input, audio_type='flac'):
    audio_file_output = str(audio_file_input) + '.' + str(audio_type)

    if parm_runtime_env_GCP:  # using Datalab in Google Cloud Platform
        # GCP: use avconv to convert audio
        retcode = subprocess.call(['avconv', '-i', audio_file_input, '-ac', '1', audio_file_output])
    else:  # using an iss-vm Virtual Machine, or local machine
        retcode = subprocess.call(['ffmpeg', '-i', audio_file_input, '-ac', '1', audio_file_output])

    if retcode == 0:
        print('[  O K  ]')
        try:
            os.remove(audio_file_input)
        except OSError as e:
            print(e)
        else:
            print("input File is deleted successfully")
    else:
        print('[ ERROR ]')

    return audio_file_output  # return file name string only

# API control parameter for  'voice to text' language


def speech2text(speech_file, language_code='en-US'):
    from google.cloud.speech import types

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(language_code=language_code)

    response = client_speech2text.recognize(config, audio)

    for result in response.results:
        response = result.alternatives[0].transcript

    try:
        os.remove(speech_file)
    except OSError as e:
        print(e)
    else:
        print("output File is deleted successfully")
    return response


def recognize(audiotext,info):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(audiotext)

    city = []
    dates = []
    adult = 0
    child_age = []
    for noun_chunk in doc.noun_chunks:
        if 'adult' in noun_chunk.lemma_:
            adult = int(noun_chunk.ents[0].text)
        if 'child' in noun_chunk.lemma_:
            num_child = int(noun_chunk.ents[0].text)

    for ent in doc.ents:
        # print('text: ',ent.text)
        if ent.label_ == 'GPE':
            city.append(ent.text)
        elif ent.label_ == 'DATE':
            raw_date = (ent.text).split(" ")
            if len(raw_date) == 3:
                dateday = (((raw_date[1].replace('st', '')).replace('nd', '')).replace('rd', '')).replace('th', '')
                datemonth = raw_date[0]
                dateyear = raw_date[2]
                final_date = dt.strptime(dateday + " " + datemonth + " " + dateyear, '%d %B %Y')
                dates.append(final_date.strftime('%d/%m/%Y'))

    num_list = []
    for token in doc:
        if token.pos_ == 'NUM':
            num_list.append(token.text)
    for i in range(num_child):
        child_age.append(num_list[-i - 1])

    # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
    info['city'] = city
    info['dates'] = dates
    info['adult'] = adult
    info['child_age'] = child_age
    print('city: ', info['city'])
    print('dates: ', info['dates'] )
    print('adult: ', info['adult'])
    print('children: ', info['child_age'])