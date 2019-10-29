import speech_recognition as sr
import os
import subprocess
import spacy
from datetime import datetime as dt

# Uncomment to run the code in local machine
parm_runtime_env_GCP = False

def audio_conversion(audio_file_input, audio_type='wav'):
    audio_file_output = str(audio_file_input) + '.' + str(audio_type)

    if parm_runtime_env_GCP:  # using Datalab in Google Cloud Platform
        # GCP: use avconv to convert audio
        retcode = subprocess.call(['avconv', '-i', audio_file_input, '-ac', '1', audio_file_output])
    else:  # using an iss-vm Virtual Machine, or local machine
        retcode = subprocess.call(['ffmpeg', '-i', audio_file_input, '-ac', '1', audio_file_output])

    if retcode == 0:
        try:
            os.remove(audio_file_input)
        except OSError as e:
            print(e)
        else:
            print("input File is deleted successfully")
    else:
        print('[ ERROR ]')

    return audio_file_output  # return file name string only

def audio2text(audiofile):
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(audiofile) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition
    try:
        print("We think you said:  " + r.recognize_google(audio))

        try:
            os.remove(audiofile)
        except OSError as e:
            print(e)
        else:
            print("output File is deleted successfully")
        return r.recognize_google(audio)

    except sr.UnknownValueError:
        print("We could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from service; {0}".format(e))

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

    for ent in doc.ents:
        #print('text: ',ent.label_)
        if ent.label_ == 'GPE':
            city.append(ent.text)
        elif ent.label_ == 'DATE' and 'age' not in ent.text:
            raw_date = (ent.text).split(" ")
            dateday = (((raw_date[1].replace('st', '')).replace('nd', '')).replace('rd', '')).replace('th', '')
            datemonth = raw_date[0]
            month = dt.strptime(datemonth, '%B')
            datemonth = month.strftime('%m')[:2]
            if len(raw_date) == 3:
                dateyear = raw_date[2]
            if len(raw_date) == 2:
                now = dt.now()
                now_year = now.strftime('%Y/%m%d %H:%M:%S')[:4]
                now_month = now.strftime('%Y/%m%d %H:%M:%S')[5:7]
                now_day = now.strftime('%Y/%m%d %H:%M:%S')[7:10]
                if now_month < datemonth:
                    dateyear = now_year
                elif now_month == datemonth and now_day <= dateday:
                    dateyear = now_year
                else:
                    dateyear = int(now_year) + 1
            final_date = dt.strptime(dateday + " " + datemonth + " " + str(dateyear), '%d %m %Y')
            dates.append(final_date.strftime('%d/%m/%Y'))

    age_is = False

    for token in doc:
        #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
        if token.lemma_ == 'age':
            age_is = True
        if age_is: # exist key word 'key word'
            if token.pos_ == 'NUM':
                child_age.append(token.text)

    info['city'] = city
    info['dates'] = dates
    info['adult'] = adult
    info['child_age'] = child_age
    return info

def find_num(text):  # use to get the num of monitor days
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    flag = 1
    for token in doc:
        if token.pos_ == 'NUM' or token.pos_ == 'X':
            flag = 0
            return int(token.text)
    if flag:
        return 1


#info = {'city': [], 'trip_type': '', 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': []}
#audiotext = "I am looking for flight from Singapore to Beijing on November 1st 2019 and returning on November 5th 2019 for 2 adults and 2 children age 2 and 4"
#audiotext = 'September 5th'
#info = recognize(audiotext, info)
#print(info)