#import pymongo
from datetime import datetime as dt

def connectDB():
    try:
        dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #dblist = dbclient.list_database_names()
        db = dbclient['FlightAssistant']
        return db
    except Exception as e:
        print(f"Error '{str(e)}' encountered")
        return False

def Request_Collection():
    try:
        db = connectDB()
        dbcollect = db['FlightRequestDetails']
        return dbcollect
    except Exception as e:
        print(f"Error '{str(e)}' encountered")
        return False

def newFlightRequest(Source,AcctRef,info,DaysMonitoring=1):
    collectReq = Request_Collection()
    ReqDT = dt.now()
    Request_ID = Source + ";" + AcctRef + ";" + ReqDT.strftime("%Y%m%d%H%M%S")
    dictReq = {"Request_ID": Request_ID, "Request_Source": Source,
               "Account_Reference": AcctRef, "Request_Datetime": ReqDT, "Request_Details": info,
               "Monitor_Days": DaysMonitoring}
    collectReq.insert_one(dictReq)
    return Request_ID

def extendFlightRequest(request_id, extendDays):
    collectReq = Request_Collection()
    ReqID = collectReq.find({"Request_ID":request_id})
    currMonitorDays = ReqID["Monitor_Days"]
    collectReq.update_one({"Request_ID": request_id}, {"$set": {"Monitor_Days": currMonitorDays+extendDays}})

def retrieve_FlightRequest(request_id=None,active=True):
    collectReq = Request_Collection()
    if request_id == None:
        if active :
            pipeline = [{'$redact':
                {'$cond': [
                    {'$and': [
                        {'$gte': [dt.now(), '$Request_Datetime']},
                        {'$lte': [dt.now(),
                                  {'$add': ['$Request_Datetime', {'$multiply': ['$Monitor_Days', 24 * 60 * 60000]}]}]}
                    ]},
                    '$$KEEP',
                    '$$PRUNE'
                ]}
            }]
            FlightRequest = collectReq.aggregate(pipeline)
        else:
            FlightRequest = collectReq.find()
    else:
        FlightRequest = collectReq.find({"Request_ID":request_id})

    return FlightRequest

def FlightDeals_Collection():
    try:
        db = connectDB()
        dbcollect = db['FlightDeals']
        return dbcollect
    except Exception as e:
        print(f"Error '{str(e)}' encountered")
        return False

def newFlightDeals(flight_main):
    collectDeal = FlightDeals_Collection()
    collectDeal.insert_one(flight_main)

def retrieve_FlightDeal(request_id,deal_index=None):
    collectDeal = FlightDeals_Collection()
    if deal_index == None:
        FlightDeal = collectDeal.find({"Request_ID":request_id})
    else:
        FlightDeal = collectDeal.find({"Request_ID":request_id,"Deal Index":deal_index})
    return FlightDeal

# Request = {"Request_ID" ,"Request_Source", "Account_Reference", "Request_Datetime", "{Request_Details}"}

# Flight Main {'Request_ID', "Result_datetime', 'Deal Index', 'Price', '{Flight Details}'}
# Flight Details {'Flight Leg', 'Bound', 'Departure Time', 'Arrival Time', 'Duration', 'Transfer', 'Transfer Place', 'Airline'}

# Current Version
# main = {'Deal': deal_lst, 'Flight Info': [[date1, trip1, date2, trip2],[date1, trip1, date2, trip2]], 'Price': price_lst, 'Hyperlink': href_lst, 'Details': {'Deal Index', 'Flight Leg', 'Bound', 'Departure Time', 'Arrival Time', 'Duration', 'Transfer', 'Transfer Place', 'Airline'}}

# Current Version
# main = {'Deal': deal_lst, 'Flight Info': [[date1, trip1, date2, trip2],[date1, trip1, date2, trip2]], 'Price': price_lst, 'Hyperlink': href_lst, 'Details': {'Deal Index', 'Flight Leg', 'Bound', 'Departure Time', 'Arrival Time', 'Duration', 'Transfer', 'Transfer Place', 'Airline'}}

