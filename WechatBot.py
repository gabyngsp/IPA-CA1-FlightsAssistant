import datetime
import time
import _thread

import itchat
from itchat.content import *

from audio2text import audio2text, audio_conversion, recognize
from skyscanner_flight_search import flight_search


info = {'city': [], 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': [], 'trip_type': ''}
enquiry = [False, False, False, False, False]
user = {'nickname': '', 'flight_info': info,'enquiry':enquiry}

user_db = []
flag = False
last_index = 0

# change the cities' order. Put the last one as departure city
def order(dates):
    temp = dates[-1]
    for i in range(len(dates) - 1, 0, -1):
        dates[i] = dates[i - 1]
    dates[0] = temp
    return dates #


def find_user(msg):
    for i in range(len(user_db)):
        if user_db[i]['nickname'] == msg['FromUserName']:
            return user_db[i]
        else:
            return 0


def update_enq(info, enquiry):
    if info['city']:
        enquiry[0] = True
    if info['dates']:
        enquiry[1] = True
    if info['cabin_class']:
        enquiry[2] = True
    if info['adult']:
        enquiry[3] = True
    if info['child_age']:
        enquiry[4] = True
    return enquiry


def ask_info(msg,enquiry):
    if not enquiry[0] and flag:  # city
        itchat.send('Input Departure city in order', msg['FromUserName'])
        last_index = 0
    elif not enquiry[1] and flag:  # dates
        itchat.send('Departure dates', msg['FromUserName'])
        last_index = 1
    elif not enquiry[2] and flag:  # cabin
        itchat.send('Your cabin class', msg['FromUserName'])
        last_index = 2
    elif not enquiry[3] and flag:  # adult
        itchat.send('How many adults? ', msg['FromUserName'])
        last_index = 3
    elif not enquiry[4] and flag:  # child
        itchat.send('If you have children, input their ages', msg['FromUserName'])
        last_index = 4
    else:
        last_index = 5
    return last_index


def update_info(msg,info):
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
            info["child_age"] = []
        else:
            for i in range(len(data)):
                info["child_age"].append(data[i])
    return info


itchat.auto_login(hotReload=True)


@itchat.msg_register([TEXT, RECORDING])  # [TEXT, MAP, CARD, NOTE, SHARING]
def book_flight(msg):
    print(u'message tpye: [ %s ] \n content: %s' % (msg['Type'], msg['Text']))
    global flag, info, enquiry, last_index,user_db
    user = {'nickname': '', 'flight_info': info, 'enquiry': enquiry}

    if msg['Type'] == 'Text':
        text = msg['Text']
    elif msg['Type'] == 'Recording':
        msg.download(msg.fileName)
        text = audio2text(audio_conversion(msg.fileName))
        #text = "I am looking for flight from Singapore to Beijing on November 1st 2019 and returning on November 5th 2019 for 2 adults and 3 children age 2 and 1"
    else:
        text = ''
    if 'flight' in text:
        flag = True
        user['nickname'] = msg['FromUserName']
        print('before recognize: ', info)
        user['flight_info'] = recognize(text, info)
        user['enquiry'] = update_enq(user['flight_info'],user['enquiry'])
        user_db.append(user)
    elif flag:
        user = find_user(msg)
        if user != 0:
            user['flight_info'] = update_info(msg, user['flight_info'])

    user['enquiry'] = update_enq(user['flight_info'], user['enquiry'])
    last_index = ask_info(msg, user['enquiry'])
    print("3: ", user['flight_info'])

    if all(user['enquiry']):
        itchat.send('Please wait for the result', msg['FromUserName'])
        print('before',user_db)
        #flight_search(cur_user['flight_info'])
        flag = False
        user['nickname'] = ''
        user['flight_info'] = {'city': [], 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': [], 'trip_type': ''}
        user['enquiry'] = [False, False, False, False, False]
        print('after',user_db)

def timer(main_scv, detail_scv, user_nickname): # main_scv & detail_scv are the scv files
    while 1:
        now = datetime.datetime.now()
        now_time = now.strftime('%Y/%m/%d %H:%M:%S')[11:]
        now_date = now.strftime('%Y/%m/%d %H:%M:%S')[:10]
        print('\r{}'.format(now_time),end = '')[11:]
        if now_time in ['20:00:00']:
            #itchat.send('test timer',toUserName= user_nickname)
            itchat.send_file(main_scv, user_nickname)
            itchat.send_file(detail_scv, user_nickname)
        time.sleep(60)


itchat.run()

#_thread.start_new_thread(itchat.run, ())
#_thread.start_new_thread(timer(), ())

# itchat.logout()

def old_version(msg, i):
    if not enquiry[0] and flag:
        itchat.send('Destination, date(day/month/year)\n End with typing: finish', msg['FromUserName'])
        if "finish" in msg['Text']:
            enquiry[0] = True
            itchat.send('Departure city', msg['FromUserName'])
        else:
            data = msg['Text'].split(',')
            info["city"].append(data[0])
            info["dates"].append(data[1])
            i = i + 1
    elif not enquiry[1] and flag:
        info["city"].append(msg['Text'])
        info["city"] = order(info["city"])
        enquiry[1] = True
        itchat.send('Your cabin class', msg['FromUserName'])
    elif not enquiry[2] and flag:
        info["cabin_class"] = msg['Text']
        enquiry[2] = True
        itchat.send('Number of adults.', msg['FromUserName'])
    elif not enquiry[3] and flag:
        info["adult"] = msg['Text']
        enquiry[3] = True
        itchat.send('If you have children? input the age', msg['FromUserName'])
    elif not enquiry[4] and flag:
        data = msg['Text'].split(",")
        if 'none' in data[0].lower() or 'no' in data[0].lower():
            info["child_age"] = []
        else:
            for i in range(len(data) - 1):
                info["child_age"].append(data[i + 1])
        enquiry[4] = True
