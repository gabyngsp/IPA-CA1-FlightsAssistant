# import requests
# #import os
# #import speech_recognition as sr
# #from pydub import AudioSegment
#
# API_ENDPOINT = 'https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
# subscription_key = '8e62901a04bc4201b0d670ed96dcc7dd'
#
# def get_token(subscription_key):
#     headers = {
#         'Ocp-Apim-Subscription-Key': subscription_key
#     }
#     response = requests.post(API_ENDPOINT, headers=headers)
#     access_token = str(response.text)
#     print(access_token)
#
# #token = get_token(subscription_key)
# response = requests.post(API_ENDPOINT, files={'fieldname':'191011-141038.mp3'},)
# print(response)
# headers = {'Ocp-Apim-Subscription-Key':subscription_key,
#            'Expect':'Expect: 100-continue',
#            'Accept':'application/json',
#            'Content-type':'audio/wav; codecs=audio/pcm; samplerate=16000'}
# res = requests.post(API_ENDPOINT,params={'format':'simple','language':'en-US'},headers = headers)
# print(res)
# #''text = data.json()['DisplayText']

# -*- coding: UTF-8 -*-
import requests
import itchat
import json
from itchat.content import *
import os
import speech_recognition as sr
from pydub import AudioSegment

BING_KEY = '8e62901a04bc4201b0d670ed96dcc7dd'

def get_response_tuling(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': '8edce3ce905a4c1dbb965e6b35c3834d',
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    except:
        # 将会返回一个None
        return


def asr():  # speech to text
    #AudioSegment.converter = "D:\Software-Agent\FlightsAssistant\\ffmpeg"
    print("www")
    song = AudioSegment.from_mp3(file='a.mp3')
    song.export("tmp.wav", format="wav")
    r = sr.Recognizer()
    with sr.AudioFile('tmp.wav') as source:
        audio = r.record(source)  # read the entire audio file
    #os.remove('tmp.wav')
    #os.remove('a.mp3')

    try:
        text = r.recognize_bing(audio, key=BING_KEY, language="en-US")
        print("Voice Recognition thinks you said " + text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results {0}".format(e))

APIKEY='AIzaSyDl5yvVJ9ArAvgZjcOE6pdvVxouvrJX5ZA'




# @itchat.msg_register(TEXT)  # 因为之前把itchat.content全部import了，里面有TEXT变量
# def tuling_reply_text(msg):
#     # 注册文字消息获取后的处理
#     # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
#     defaultReply = 'I received a: ' + msg['Text']
#     return get_response_tuling(msg['Text']) or defaultReply
#
#
# @itchat.msg_register(RECORDING)
# def tuling_reply(msg):
#     # 注册语音消息获取后的处理
#     # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
#     defaultReply = 'I received a: ' + msg['Type']
#
#     # 如果图灵Key出现问题，那么reply将会是None
#     asrMessage = asr(msg)
#     return get_response_tuling(asrMessage) or defaultReply
