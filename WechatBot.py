import itchat
from itchat.content import *

from DB_Functions import newFlightRequest
from audio2text import audio2text, audio_conversion, recognize, find_num


info = {'city': [], 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': [], 'trip_type': ''}
enquiry = [False, False, False, False, False]
confrim = [False, False, False, False, False]


user_db = []
flag = False
confirm = False
flag2 = False  # flag for ask monitor days
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

def update_info(msg, info):
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

# confirm all the new info if correct
def ask_confirm(text,nickname):
    if not enquiry[0] and confirm[0]:  # city
        itchat.send('Confirm\nCity:'+text.split(','),nickname)
    if not enquiry[1] and confirm[1]:  # dates
        if ',' in text:
            itchat.send('Confirm\nDates:'+text.split(','),nickname)
        else:
            itchat.send('Confirm\nDates:'+text,nickname)
    if not enquiry[2] and confirm[2]:  # cabin class
        itchat.send('Confirm\nCabin class:'+text,nickname)
    if not enquiry[3] and confirm[3]:  # adult
        itchat.send('Confirm\nAdult:'+text,nickname)
    if not enquiry[4] and confirm[4]:  # children
        data = text.split(",")
        if 'none' in data[0].lower() or 'no' in data[0].lower():
            itchat.send('Confirm\nNo children',nickname)
        else:
            itchat.send('Confirm\nChildren age:' + data, nickname)


def confirm_info(text):
    if 'yes' in text:
        return True
    else:
        return False



def getMonitorday(text):
    return find_num(text)

itchat.auto_login(hotReload=True)


@itchat.msg_register([TEXT, RECORDING])  # [TEXT, MAP, CARD, NOTE, SHARING]
def book_flight(msg):
    print(u'message tpye: [ %s ] \n content: %s' % (msg['Type'], msg['Text']))
    global flag, info, enquiry, last_index, user_db, flag2, confirm
    user = {'nickname': '', 'flight_info': info, 'enquiry': enquiry,'confirm': confirm,'monitor_day':0}

    if msg['Type'] == 'Text':
        text = msg['Text']
    elif msg['Type'] == 'Recording':
        #msg.download(msg.fileName)
        #text = audio2text(audio_conversion(msg.fileName))
        text = "I am looking for flight from Singapore to Beijing on November 1st 2019 and returning on November 5th 2019 for 2 adults and 3 children age 2 and 1"
    else:
        text = ''
    if 'flight' in text:
        flag = True
        user['nickname'] = msg['FromUserName']
        # need to confirm
        user['flight_info'] = recognize(text, info)
        confirm = update_enq(user['flight_info'],user['enquiry'])
        ask_confirm(text)
        user_db.append(user)
    elif flag:
        user = find_user(msg)
        if user != 0:
            if confirm: # need to confirm
                confirm_info(msg)
                comfirm = confirm_info(text)
            else:  # ask next question
                user['flight_info'] = update_info(msg, user['flight_info'])

    user['enquiry'] = update_enq(user['flight_info'], user['enquiry'])
    last_index = ask_info(msg, user['enquiry'])
    print("3: ", user['flight_info'])
    if flag2:
        days = getMonitorday(text)
        user['monitor_day'] = days
    if all(user['enquiry']) and not flag2:
        itchat.send('How many days do you need?', msg['FromUserName'])
        flag2 = True
    if user['monitor_day']:
        itchat.send('Please wait for the result', msg['FromUserName'])
        print('before',user_db)
        newFlightRequest('wechat', user['nickname'], user['flight_info'], user['monitor_day'])
        flag = False
        flag2 = False
        user['nickname'] = ''
        user['flight_info'] = {'city': [], 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': [], 'trip_type': ''}
        user['enquiry'] = [False, False, False, False, False]
        user['monitor_day'] = 0
        print('after',user_db)

def timer(main_scv, detail_scv, user_nickname): # main_scv & detail_scv are the scv files
    itchat.send_file(main_scv, user_nickname)
    itchat.send_file(detail_scv, user_nickname)


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
