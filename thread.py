import datetime
import threading
import time
# from queue import Queue
import itchat

from WechatBot import wechat
from batch_search import batch_search


def chatbot():
    wechat()
    # out_q.put(data)

# A thread that consumes data
def search():
    time.sleep(3)
    # data = in_q.get()
    while 1:
        now = datetime.datetime.now()
        now_str = now.strftime('%Y/%m/%d %H/%M/%S')[11:]
        print(now_str)
        if now_str in '08/00/00':  # %h/%m/%s
            print('time to do batch search')
            batch_search()
        if now_str in '10/00/00':
            print('time to send files')
            itchat.send('test timer', toUserName="filehelper")
            # itchat.send_file(outfile, nickname)
        time.sleep(30)

# Create the shared queue and launch both threads
#q = Queue()
t1 = threading.Thread(target=chatbot)
t2 = threading.Thread(target=search)
t1.start()
t2.start()

# class flight(threading.Thread):
#     def __init__(self, num):
#         threading.Thread.__init__(self)
#         self._run_num = num
#
#     def run(self):
#         # batch_search()
#         for i in range(10):
#             print('search use request id: '+str(self._run_num))
#
#
# class wechat_bot(threading.Thread):
#   def run(self):
#       for i in range(10):
#           req_id = '200'
#           print('wechat get request id: '+req_id)
#       #wechat()
#
#
if __name__ == '__main__':
    req_id = '1'
    threads = []
    # threads.append(flight())
    threads.append(wechat_bot())
    threads.append(flight(req_id))
    for t in threads:
        t.start()
    for t in threads:
        t.join()