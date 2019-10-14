import pandas as pd
import tagui as t
import tagui_util as util
from pandas import DataFrame
from datetime import datetime, timedelta

t.close()
t.init()
url2 = 'https://www.skyscanner.com.sg/transport/flights/sins/dlc/191118/191120/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home'
url1 = 'https://www.skyscanner.com.sg/transport/flights/sins/bjsa/191019/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home'
url3 = 'https://www.skyscanner.com.sg/transport/flights/sins/dlc/191118/191120/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home'
t.url('url3')
date = ['2019-11-18', '2019-11-20', '2019-11-24']
ind = 0

def getFlightInfo(date, url, ind):
    util.wait_for_pageload('//div[@class="ResultsSummary_summaryContainer__3_ZX_"]//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT SummaryInfo_itineraryCountContainer__30Hjd"]')

    time_dep_lst = []
    time_arr_lst = []
    time_arr_day_lst = []
    airline_lst = []
    dur_lst = []
    price_lst = []
    transfer_lst = []
    transfer_plc_lst = []
    href_lst = []
    flight1_lst = ['', '']
    flight2_lst = ['', '']
    flight3_lst = ['', '']
    bound_lst = []
    deal_lst = []
    index_lst = []
    leg_lst = []
    date1_lst = []
    date2_lst = []
    date3_lst = []
    m = 1
    type = len(date)
    ###Sponsor check
    for n in range(2):
        if t.present('//span[@class="BpkBadge_bpk-badge__2mEjm "]'):
            k = n + 1
        else:
            k = n

        ### href and price check
        href = util.hover_and_read(f'(//a[@class="FlightsTicket_link__kl4DL"])[{n + 1}]//@href')
        price = util.hover_and_read(f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN BpkText_bpk-text--bold__4yauk"])[{k + 4}]')

        ind = ind + 1
        print(ind)

        for i in range(type):
            leg = i
            time_dep = util.hover_and_read(f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN"])[{2* type * n + 1 + 2 * i}]')
            time_arr = util.hover_and_read(f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN"])[{2* type * n + 2 + 2 * i}]')
            airline = util.hover_and_read(f'(//img[@class="BpkImage_bpk-image__img__3HwXN"])[{type * k + 2 + i}]/@alt')
            dur = util.hover_and_read(f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT Duration_duration__1QA_S"])[{type * n + 1 + i}]')
            transfer = util.hover_and_read(f'(//div[@class="LegInfo_stopsLabelContainer__2dEdt"]/span)[{type * n + 1 + i}]')
            if transfer == 'Direct':
                transfer_plc = ''
            elif transfer == '1 stop':
                transfer_plc = util.hover_and_read(f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT LegInfo_stopStation__Ec5OU"])[{m}]')
                m = m + 1

            ### Arrival Time plus 1 day check
            if t.present('(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN LegInfo_routePartialTime__2HfzB"])[' + str(2 * type * n + 2 + 2 * i) + ']//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT TimeWithOffsetTooltip_offsetTooltip__24Ffv"]'):
                date_pls = 1
            else:
                date_pls = 0

            ### Bound Check
            dep = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--base__2vfTl LegInfo_routePartialCityTooltip__ZqOZK"])[{2* type * n + 1 + 2 * i}]')
            arr = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--base__2vfTl LegInfo_routePartialCityTooltip__ZqOZK"])[{2 * type * n + 2 + 2 * i}]')
            bound = dep + ' - ' + arr
            bound_lst.append(bound)
            if i == 0:
                flight1_lst[n] = bound_lst[type * n]
                date_time_dep = date[0] + ' ' + time_dep
                datetime_dep = datetime.strptime(date_time_dep, "%Y-%m-%d %H:%M")
                time_dep_lst.append(datetime_dep)
                date_time_arr = date[0] + ' ' + time_arr
                if date_pls == 0:
                    datetime_arr = datetime.strptime(date_time_arr, "%Y-%m-%d %H:%M")
                else:
                    datetime_arr = datetime.strptime(date_time_arr, "%Y-%m-%d %H:%M") + timedelta(days=1)
                time_arr_lst.append(datetime_arr)
            elif i == 1:
                flight2_lst[n] = bound_lst[type * n + 1]
                date_time_dep = date[1] + ' ' + time_dep
                datetime_dep = datetime.strptime(date_time_dep, "%Y-%m-%d %H:%M")
                time_dep_lst.append(datetime_dep)
                date_time_arr = date[1] + ' ' + time_arr
                if date_pls == 0:
                    datetime_arr = datetime.strptime(date_time_arr, "%Y-%m-%d %H:%M")
                else:
                    datetime_arr = datetime.strptime(date_time_arr, "%Y-%m-%d %H:%M") + timedelta(days=1)
                time_arr_lst.append(datetime_arr)
            elif i == 2:
                flight3_lst[n] = bound_lst[type * n + 2]
                date_time_dep = date[2] + ' ' + time_dep
                datetime_dep = datetime.strptime(date_time_dep, "%Y-%m-%d %H:%M")
                time_dep_lst.append(datetime_dep)
                date_time_arr = date[2] + ' ' + time_arr
                if date_pls == 0:
                    datetime_arr = datetime.strptime(date_time_arr, "%Y-%m-%d %H:%M")
                else:
                    datetime_arr = datetime.strptime(date_time_arr, "%Y-%m-%d %H:%M") + timedelta(days=1)
                time_arr_lst.append(datetime_arr)

            airline_lst.append(airline)
            dur_lst.append(dur)
            time_arr_day = ''
            time_arr_day_lst.append(time_arr_day)
            transfer_lst.append(transfer)
            transfer_plc_lst.append(transfer_plc)
            leg_lst.append(leg)
            index_lst.append(ind)

        date1_lst.append(date[0])
        date2_lst.append(date[1])
        date3_lst.append(date[2])
        href_lst.append(url + href)
        price_lst.append(price)
        deal_lst.append(ind)
        details = {'Deal Index': index_lst, 'Flight Leg': leg_lst, 'Bound': bound_lst, 'Departure Time': time_dep_lst,
                   'Arrival Time': time_arr_lst, 'Duration': dur_lst, 'Transfer': transfer_lst,
                   'Transfer Place': transfer_plc_lst, 'Airline': airline_lst}
        main = {'Deal': deal_lst, 'Flight1 Date': date1_lst, 'Flight1': flight1_lst, 'Flight2 Date': date2_lst,
                'Flight2': flight2_lst, 'Flight3 Date': date3_lst,
                'Flight3': flight3_lst, 'Price': price_lst, 'Hyperlink': href_lst}
    return main, details, ind


frames_main = []
frames_details = []
flight_main, flight_details, ind = getFlightInfo(date, url3, ind)
#flight_main, flight_details, ind = getFlightInfo(date, url1, ind)
frames_details.append(DataFrame(flight_details,
                                columns=['Deal Index', 'Flight Leg', 'Bound', 'Departure Time', 'Arrival Time', 'Duration', 'Transfer', 'Transfer Place', 'Airline']))
df_details = pd.concat(frames_details)

export_csv = df_details.to_csv('Skyscanner_details.csv', index=None)
print(df_details)

frames_main.append(DataFrame(flight_main,
                             columns=['Deal', 'Flight1 Date', 'Flight1', 'Flight2 Date', 'Flight2', 'Flight3 Date', 'Flight3', 'Price', 'Hyperlink']))
df_main = pd.concat(frames_main)

export_csv = df_main.to_csv('Skyscanner_main.csv', index=None)
print(df_main)
