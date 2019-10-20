import itchat
from itchat.content import *

from audio2text import audio2text, audio_conversion, recognize
from skyscanner_flight_search import flight_search

info = {'city': [], 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': [], 'trip_type': ''}
enquiry = [False, False, False, False, False]
flag = False
i = 0
last_index = 0


def order(dates):
    temp = dates[-1]
    for i in range(len(dates) - 1, 0, -1):
        dates[i] = dates[i - 1]
    dates[0] = temp
    return dates


def update_enq():
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


def ask_info(msg):
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


def update_info(msg):
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
    global flag, info, enquiry, last_index

    if msg['Type'] == 'Text':
        text = msg['Text']
    if msg['Type'] == 'Recording':
        # msg.download(msg.fileName)
        # text = audio2text(audio_conversion(msg.fileName))
        text = "I am looking for flight from Singapore to Beijing on November 1st 2019 and returning on November 5th 2019"

    if 'flight' in text:
        flag = True
        info = recognize(text, info)
        update_enq()
    else:
        info = update_info(msg)
    update_enq()
    last_index = ask_info(msg)
    print("3: ",info)

    if all(enquiry):
        itchat.send('Please wait for the result', msg['FromUserName'])
        print(info)
        # flight_search(info)
        # itchat.send_file('Skyscanner_details.csv', msg['FromUserName'])
        # itchat.send_file('Skyscanner_main.csv', msg['FromUserName'])
        flag = False
        info = {'city': [], 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': [], 'trip_type': ''}
        enquiry = [False, False, False, False, False]


itchat.run()


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
