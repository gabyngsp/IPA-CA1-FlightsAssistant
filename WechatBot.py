import itchat
from itchat.content import *
from skyscanner_flight_search import flight_search

itchat.auto_login(hotReload=True)

# username = itchat.search_friends(name=u'伦家小Yanni')[0]['UserName']


info = {'city': [], 'trip_type': '', 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': []}
enquiry = [False, False, False, False, False]
flag = False
i = 0


def order(dates):
    temp = dates[-1]
    for i in range(len(dates)-1,0,-1):
        dates[i] = dates[i-1]
    dates[0] = temp
    return dates


@itchat.msg_register([TEXT])  # [TEXT, MAP, CARD, NOTE, SHARING] 文字、位置、名片、通知、分享
def book_flight(msg):
    print(u'message tpye: [ %s ] \n content: %s' % (msg['Type'], msg['Text']))
    global flag, info, enquiry, result, city_enquiry, i

    if "book flights" in msg['Text']:
        flag = True
        itchat.send('Destination, date(day/month/year)\n End with typing: finish', msg['FromUserName'])
    elif not enquiry[0] and flag:
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
            print("here")
            for i in range(len(data)-1):
                info["child_age"].append(data[i+1])
        enquiry[4] = True

    if all(enquiry):
        itchat.send('Please wait for the result', msg['FromUserName'])
        print(info)
        #flight_search(info)
        #itchat.send_file('Skyscanner.csv', msg['FromUserName'])
        flag = False
        i = 0
        info = {'city': [], 'trip_type': '', 'dates': [], 'cabin_class': '', 'adult': '', 'child_age': []}
        enquiry = [False, False, False, False, False]


itchat.run()
# itchat.logout()
