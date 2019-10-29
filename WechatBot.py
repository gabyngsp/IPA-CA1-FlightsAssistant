import datetime
import time

import itchat
from itchat.content import *

from DB_Functions import newFlightRequest, retrieve_FlightRequest
from audio2text import audio2text, audio_conversion, recognize, find_num
from skyscanner_flight_search import flight_search

user_db = []


# change the cities' order. Put the last one as departure city
def order(dates):
    temp = dates[-1]
    for i in range(len(dates) - 1, 0, -1):
        dates[i] = dates[i - 1]
    dates[0] = temp
    return dates  #

def getuserid(nickname):
    info_user = itchat.search_friends(nickname)
    return info_user[0]['UserName']

def find_user(msg):
    for i in range(len(user_db)):
        if user_db[i]['nickname'] == msg['User']['NickName']:
            return i
    return -1


def update_enq(info, enquiry):
    if info['city']:
        enquiry[0] = True
    if info['dates']:
        enquiry[1] = True
    if info['cabin_class']:
        enquiry[2] = True
    if info['adult']:
        enquiry[3] = True
    if info['child_age']:  ####
        enquiry[4] = True
    return enquiry


def ask_info(msg, enquiry):
    if not enquiry[0]:  # city
        itchat.send('Input Departure city in order', msg['FromUserName'])
        last_index = 0
    elif not enquiry[1]:  # dates
        itchat.send('Departure dates', msg['FromUserName'])
        last_index = 1
    elif not enquiry[2]:  # cabin
        itchat.send('Your cabin class', msg['FromUserName'])
        last_index = 2
    elif not enquiry[3]:  # adult
        itchat.send('How many adults? ', msg['FromUserName'])
        last_index = 3
    elif not enquiry[4]:  # child
        itchat.send('If you have children, input their ages', msg['FromUserName'])
        last_index = 4
    else:
        last_index = 5
    return last_index


def update_info(msg, info, last_index):
    if last_index == 0:  # city
        info["city"] = msg['Text'].split(',')
    if last_index == 1:  # dates
        if ',' in msg['Text']:
            info["dates"] = msg['Text'].split(',')
        else:
            info["dates"] = msg['Text']
    if last_index == 2:  # cabin class
        info["cabin_class"] = msg['Text']
    if last_index == 3:  # adult
        info["adult"] = msg['Text']
    if last_index == 4:  # children
        data = msg['Text'].split(",")
        if 'none' in data[0].lower() or 'no' in data[0].lower():
            info["child_age"] = ['0']
        else:
            for i in range(len(data)):
                info["child_age"].append(data[i])
    return info


def list2str(l):
    str = ''
    for e in l:
        str += e + ' '
    return str


# confirm all the new info if correct
def ask_confirm(user):
    info = user['flight_info']
    confirm_msg = 'Confirm\ncity: ' + list2str(info['city'])+'\ndates: ' + list2str(info['dates'])+'\ncabin class: ' + info['cabin_class']+'\nadult number: ' + str(info['adult'])+'\nchildren age: ' + list2str(info['child_age'])+'\nmonitor days: '+str(user['monitor_day'])
    #print(confirm_msg)
    itchat.send(confirm_msg, getuserid(user['nickname']))


def confirm_info(text,user):
    if 'yes' in text.lower() or 'ok' in text.lower():
        return True
    else:
        fix_info(text,user)
        return False


def fix_info(text,user):
    multi_data = text.split('.') # different info
    for d in multi_data:
        data = d.split(':') # extract info
        print(data)
        if 'city' in data[0].lower():  # city
            user['flight_info']["city"] = data[1].split(',')
        if 'dates' in data[0].lower():  # dates
            if ',' in data[1]:
                user['flight_info']["dates"] = data[1].split(',')
            else:
                user['flight_info']["dates"] = data[1]
        if 'class' in data[0].lower():  # cabin class
            user['flight_info']["cabin_class"] = data[1]
        if 'adult' in data[0].lower(): # adult
            user['flight_info']["adult"] = data[1]
        if 'children' in data[0].lower():  # children
            data = data[1].split(",")
            if 'none' in data[0].lower() or 'no' in data[0].lower():
                user['flight_info']["child_age"] = ['0']
            else:
                for i in range(len(data)):
                    user['flight_info']["child_age"]=[]
                    user['flight_info']["child_age"].append(data[i])


def getMonitorday(text):
    return find_num(text)


@itchat.msg_register([TEXT, RECORDING])  # [TEXT, MAP, CARD, NOTE, SHARING]
def book_flight(msg):
    print(u'message tpye: [ %s ] \n content: %s' % (msg['Type'], msg['Text']))
    global user_db
    info = {'city': [], 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': [], 'trip_type': ''}
    enquiry = [False, False, False, False, False]
    user = {'nickname': '', 'flight_info': info, 'enquiry': enquiry, 'flag_monitor': False, 'flag_confirm': False,
            'last_index': 0, 'monitor_day': '0'}
    monitor = False

    if msg['Type'] == 'Text':
        text = msg['Text']
    elif msg['Type'] == 'Recording':
        msg.download(msg.fileName)
        text = audio2text(audio_conversion(msg.fileName,bitrate='24k'))
        # text = audio2text(audio_conversion(msg.fileName, bitrate='32k'))
    else:
        text = ''

    index = find_user(msg)
    if index != -1:  # user exists
        user = user_db[index]
        user['flight_info'] = update_info(msg, user['flight_info'], user['last_index'])
    elif 'flight' in text:
        user['nickname'] = msg['User']['NickName']
        user['flight_info'] = recognize(text, user['flight_info'])
        user_db.append(user)
        index = find_user(msg)

    if index != -1:  # in the searching process
        user['enquiry'] = update_enq(user['flight_info'], user['enquiry'])
        user['last_index'] = ask_info(msg, user['enquiry'])
        print("*1* ", user)

    if user['flag_monitor'] and user['monitor_day']== '0':  # get monitor days
        days = getMonitorday(text)
        print("monitor days: " + str(days))
        user['monitor_day'] = str(days)
        monitor = True
    elif all(user['enquiry']) and not user['flag_monitor']:
        print('monitor days')
    #############
        itchat.send('Monitor days?', getuserid(user['nickname']))
        user['flag_monitor'] = True

    if user['monitor_day'] != '0' and not user['flag_confirm']:
        if not monitor:
            print('get the update info')
            user['flag_confirm'] = confirm_info(text,user)
        if not user['flag_confirm']:
            print('confirm info')
            ask_confirm(user)

    if user['flag_confirm']:  # all the info has been confirm
        if user['flight_info']['child_age'][0] == '0':
            user['flight_info']['child_age'] = []
        itchat.send('Please wait for the result', getuserid(user['nickname']))
        print('before', user_db)
        # send the new request to data base
        req_id = newFlightRequest('wechat', user['nickname'], user['flight_info'], user['monitor_day'])
        print(req_id)
        user_db.remove(user)
        user['enquiry'] = [False, False, False, False, False]
        print('after', user_db)


def wechat():
    itchat.auto_login(hotReload=True)
    data = itchat.run()
    return data


if __name__ == '__main__':
    wechat()

# itchat.logout()
