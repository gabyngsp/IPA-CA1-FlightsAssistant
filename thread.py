import threading

from WechatBot import wechat
from batch_search import batch_search
# from skyscanner_flight_search import flight_search


class flight(threading.Thread):
  def run(self):
      batch_search()
      # request = {"Request_ID": "WeChat;gongyifei;20191019223114",
      #            "Request_Details": {'city': ['singapore', 'melbourne'], 'trip_type': '',
      #                                'dates': ['19/11/2019', '25/11/2019'], 'cabin_class': 'economy', 'adult': '2',
      #                                'child_age': [1, 3]}}
      # flight_search(request)

class wechat_bot(threading.Thread):
  def run(self):
      wechat()

if __name__ == '__main__':
  threads = []
  threads.append(wechat_bot())
  threads.append(flight())
  for t in threads:
      t.start()
  for t in threads:
      t.join()