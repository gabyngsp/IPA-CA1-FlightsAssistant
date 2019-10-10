import itchat
import tagui as t
from itchat.content import *
#itchat.auto_login()
itchat.auto_login(hotReload=True)

#username = itchat.search_friends(name=u'伦家小Yanni')[0]['UserName']
#itchat.send_file('1.xlsx',toUserName=username)
t.init()
t.url('https://www.skyscanner.com.sg/')

info = {"from":"","to":"","start_date":"","end_date":"","trip_type":""}
enquiry = [False,False,False,False,False]  # depart ,dest, start date, end date, type
flag = False


@itchat.msg_register([TEXT])  # [TEXT, MAP, CARD, NOTE, SHARING] 文字、位置、名片、通知、分享
def book_flight(msg):
    print(u'message tpye: [ %s ] \n content: %s' % (msg['Type'], msg['Text']))
    global flag, info, enquiry, result

    if "book flights" in msg['Text']:
        flag = True
        itchat.send('Your departure city.', msg['FromUserName'])
        return info
    elif not enquiry[0] and flag:
        info["from"] = msg['Text']
        enquiry[0] = True
        itchat.send('Your destination city.', msg['FromUserName'])
    elif not enquiry[1] and flag:
        info["to"] = msg['Text']
        enquiry[1] = True
        itchat.send('Your start date.', msg['FromUserName'])
    elif not enquiry[2] and flag:
        info["start_date"] = msg['Text']
        enquiry[2] = True
        itchat.send('Your end date.', msg['FromUserName'])
    elif not enquiry[3] and flag:
        info["end_date"] = msg['Text']
        enquiry[3] = True
        itchat.send('Your ticket type\n 1.One way\n 2.Return\n 3.Multi-City.', msg['FromUserName'])
    elif not enquiry[4] and flag:
        info["trip_type"] = msg['Text']
        enquiry[4] = True
    if all(enquiry):
        flag = False
        result = info
        info = {"from": "", "to": "", "start_date": "", "end_date": "", "trip_type": ""}
        enquiry = [False, False, False, False, False]
        itchat.send('Please wait for the result', msg['FromUserName'])
        print(result)

itchat.run()
#itchat.logout()