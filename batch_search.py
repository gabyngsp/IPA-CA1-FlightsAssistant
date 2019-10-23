from datetime import datetime as dt
import DB_Functions as dbf
from skyscanner_flight_search import flight_search
import Skyscanner_getFlightInfo

#set Batch Job Run Date
batchRunDate = dt.now()

print(f'Batch Job Run Date: {batchRunDate}')
ReqDoc = dbf.retrieve_FlightRequest()

for row in ReqDoc:
    print(row)
    request_id = row['Request_ID']
    info = row['Request_Details']
    flight_search(row)











