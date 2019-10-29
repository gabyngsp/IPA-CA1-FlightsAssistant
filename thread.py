import datetime
import re
import threading
import time
import os
from datetime import datetime as dt
# from queue import Queue
import itchat

from DB_Functions import retrieve_FlightDeal, retrieve_FlightRequest
from WechatBot import wechat
from batch_search import batch_search
from skyscanner_flight_search import flight_search


def chatbot():
    wechat()
    # out_q.put(data)

# A thread that consumes data
def search():
    time.sleep(5)
    # data = in_q.get()
    while 1:
        now = datetime.datetime.now()
        now_str = now.strftime('%Y/%m/%d %H/%M/%S')[11:]
        print(now_str)
        #req = retrieve_FlightRequest('wechat;3af4fa015765b8e2bc1f6f22ba881a00;20191029144648')
        #flight_search(req)
        res = re.search(r'16/36/[0-9][0-9]',now_str)  # start at 08:00 - 08:01
        if True:
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
                itchat.send_file(final_path, toUserName=info_user['UserName'])
        time.sleep(50)

# Create the shared queue and launch both threads
#q = Queue()
t1 = threading.Thread(target=chatbot)
t2 = threading.Thread(target=search)
t1.start()
t2.start()
