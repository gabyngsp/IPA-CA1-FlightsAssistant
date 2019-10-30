import re

import speech_recognition as sr
import os
from pydub import AudioSegment
import subprocess
import spacy
from datetime import datetime as dt


def audio_conversion(audio_file_input,bitrate, audio_type='wav'):
    audio_file_output = str(audio_file_input).split('.')[0] + '.' + str(audio_type)
    song = AudioSegment.from_mp3(audio_file_input)
    song.export(audio_file_input, bitrate=bitrate, format="mp3")
    retcode = subprocess.call(['ffmpeg', '-i', audio_file_input, '-ac', '1', audio_file_output])

    if retcode == 0:
        print('[ OK ]')
        try:
            os.remove(audio_file_input)
        except OSError as e:
            print(e)
        else:
            print("input File")
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
            print("output File")
        return r.recognize_google(audio)

    except sr.UnknownValueError:
        print("We could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from service; {0}".format(e))

def recognize(audiotext,info):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(audiotext)

    city = info['city']
    dates = info['dates']
    adult = info['adult']
    child_age = info['child_age']

    for noun_chunk in doc.noun_chunks:
        if 'adult' in noun_chunk.lemma_:
            adult = int(noun_chunk.ents[0].text)

    for ent in doc.ents:
        #print('text: ',ent.label_)
        if ent.label_ == 'GPE':
            city.append(ent.text)
        elif ent.label_ == 'DATE' and 'age' not in ent.text:
            t = (ent.text).replace('and',',')
            date_list = t.split(",")
            print(date_list)
            for or_dates in date_list:
                raw_date = or_dates.split(" ")
                for e in raw_date:
                    if e == '':
                        raw_date.remove(e)
                dateday = ((((raw_date[1].replace('st', '')).replace('nd', '')).replace('rd', '')).replace('th', '')).replace(' ', '')
                datemonth = raw_date[0]
                month = dt.strptime(datemonth, '%B')
                datemonth = month.strftime('%m')[:2]
                dateyear = '2019'
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

    city_nondu = []
    for c in city:
        if c not in city_nondu:
            city_nondu.append(c)
    print(city_nondu)
    info['city'] = city_nondu

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

# info = {'city': [], 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': [], 'trip_type': ''}
# recognize('from dalian to beijing on November 1st, beijing to singapore on November 3rd, singapore to shenzhen on November 5th',info)
# print(info)