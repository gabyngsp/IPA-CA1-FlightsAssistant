from datetime import datetime as dt
from SystemCode import DB_Functions as dbf
from SystemCode.skyscanner_flight_search import flight_search


def batch_search():
    #set Batch Job Run Date
    batchRunDate = dt.now()

    print(f'Batch Job Run Date: {batchRunDate}')
    ReqDoc = dbf.retrieve_FlightRequest()

    for row in ReqDoc:
        print(row['Account_Reference'])
        flight_search(row)


if __name__ == '__main__':
    batch_search()