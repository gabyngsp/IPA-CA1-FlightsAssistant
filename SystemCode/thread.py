import datetime
import re
import threading
import time
import os
import json
from datetime import datetime as dt
import itchat
from SystemCode.WechatBot import wechat
from SystemCode.batch_search import batch_search


def chatbot():
    wechat()

# A thread that consumes data
def search(start_time):
    time.sleep(5)
    while 1:
        now = datetime.datetime.now()
        now_str = now.strftime('%Y/%m/%d %H/%M/%S')[11:16]
        print(now_str)
        res = re.search(start_time,now_str)
        if res:
            print('time to do batch search')
            batch_search()
            print('time to send files')
            filepath = os.path.join('batchfiles', dt.today().strftime("%Y%m%d"))
            file_list = os.listdir(filepath)
            # print(file_list)
            for outfile in file_list:
                # print(outfile)
                nickname = outfile.split('_')[1]
                print(nickname)
                final_path = os.path.join(filepath,outfile)
                print(final_path)
                info_user = itchat.search_friends(nickname)
                # print(info_user['UserName'])
                itchat.send_file(final_path, toUserName=info_user[0]['UserName'])
        time.sleep(50)


with open('configure.txt') as json_file:
    data = json.load(json_file)
    start_time = data['start_time']

t1 = threading.Thread(target=chatbot)
t2 = threading.Thread(target=search,args=(start_time,))
t1.start()
t2.start()
