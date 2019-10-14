import itchat
from itchat.content import *
from skyscanner_flight_search import flight_search

itchat.auto_login(hotReload=True)

#username = itchat.search_friends(name=u'伦家小Yanni')[0]['UserName']
#itchat.send_file('1.xlsx',toUserName=username)


info = {'from': '', 'to': '', 'trip_type': '', 'start_date': '','end_date': '', 'cabin_class': '', 'pax': ''}
enquiry = [False, False, False, False, False, False, False]
flag = False


@itchat.msg_register([TEXT])  # [TEXT, MAP, CARD, NOTE, SHARING] 文字、位置、名片、通知、分享
def book_flight(msg):
    print(u'message tpye: [ %s ] \n content: %s' % (msg['Type'], msg['Text']))
    global flag, info, enquiry, result

    if "book flights" in msg['Text']:
        flag = True
        itchat.send('Your departure city.', msg['FromUserName'])
    elif not enquiry[0] and flag:
        info["from"] = msg['Text']
        enquiry[0] = True
        itchat.send('Your destination city.', msg['FromUserName'])
    elif not enquiry[1] and flag:
        info["to"] = msg['Text']
        enquiry[1] = True
        itchat.send('Your ticket type\n 1.Return\n 2.One way\n 3.Multi-City.', msg['FromUserName'])
    elif not enquiry[2] and flag:
        info["trip_type"] = msg['Text']
        enquiry[2] = True
        itchat.send('Your start date.', msg['FromUserName'])
    elif not enquiry[3] and flag:
        info["start_date"] = msg['Text']
        enquiry[3] = True
        if '1' in info["trip_type"]:
            itchat.send('Your end date.', msg['FromUserName'])
        else:
            enquiry[4] = True
            itchat.send('Your cabin_class', msg['FromUserName'])
    elif not enquiry[4] and flag:
        info["end_date"] = msg['Text']
        enquiry[4] = True
        itchat.send('Your cabin_class', msg['FromUserName'])
    elif not enquiry[5] and flag:
        info["cabin_class"] = msg['Text']
        enquiry[5] = True
        itchat.send('2 Adults;2 Children;2,3', msg['FromUserName'])
    elif not enquiry[6] and flag:
        info["pax"] = msg['Text']
        enquiry[6] = True

    if all(enquiry):
        flag = False
        itchat.send('Please wait for the result', msg['FromUserName'])
        print(info)
        flight_search(info)
        itchat.send_file('Skyscanner.csv', msg['FromUserName'])
        info = {'from': '', 'to': '', 'trip_type': '', 'start_date': '','end_date': '', 'cabin_class': '', 'pax': ''}
        enquiry = [False, False, False, False, False, False, False]

itchat.run()
#itchat.logout()