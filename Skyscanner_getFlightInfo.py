import pandas as pd
import tagui as t
import tagui_util as util
from pandas import DataFrame
from datetime import datetime, timedelta
from Expedia_getFlightPrice import getExpFlightPrice

def getFlightInfo(date, ind):
    t.wait(2)
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
    bound_lst = []
    deal_lst = []
    index_lst = []
    leg_lst = []
    m = 1
    type = len(date)
    date_lst = []
    time_lst = []

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
            leg = i+1
            print(leg)
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

            time_lst.append(time_dep)
            date_time_dep = date[i] + ' ' + time_dep
            datetime_dep = datetime.strptime(date_time_dep, "%d/%m/%Y %H:%M")
            time_dep_lst.append(datetime_dep)
            date_time_arr = date[i] + ' ' + time_arr
            if date_pls == 0:
                datetime_arr = datetime.strptime(date_time_arr, "%d/%m/%Y %H:%M")
            else:
                datetime_arr = datetime.strptime(date_time_arr, "%d/%m/%Y %H:%M") + timedelta(days=1)
            time_arr_lst.append(datetime_arr)

            airline_lst.append(airline)
            dur_lst.append(dur)
            time_arr_day = ''
            time_arr_day_lst.append(time_arr_day)
            transfer_lst.append(transfer)
            transfer_plc_lst.append(transfer_plc)
            leg_lst.append(leg)
            index_lst.append(ind)


        href_lst.append(t.url()[0:-2] + href)
        price_lst.append(price)
        deal_lst.append(ind)

    details = {'Deal Index': index_lst, 'Flight Leg': leg_lst, 'Bound': bound_lst, 'Departure Time': time_dep_lst,
                   'Arrival Time': time_arr_lst, 'Duration': dur_lst, 'Transfer': transfer_lst,
                   'Transfer Place': transfer_plc_lst, 'Airline': airline_lst}
    main = {'Deal': deal_lst, 'Price': price_lst, 'Hyperlink': href_lst}
    return main, details, time_lst, ind


def getFlightExcel(info,ind):
    frames_main = []
    frames_details = []
    price_exp_lst = []
    flight_main, flight_details, time_lst, ind = getFlightInfo(info['dates'], ind)

    ###Compare Price with Expedia (Hyperlink/Multi to be added)
    for i in range(2):
        if len(info['dates']) == 1:
            price = getExpFlightPrice(flight_details['Airline'][i], time_lst[i], flight_details['Duration'][i])
            price_exp_lst.append(price)
            print(price_exp_lst)
        elif len(info['dates']) == 2:

            time_ref = [time_lst[2*i], time_lst[2*i + 1]]
            dur_ref = [flight_details['Duration'][2*i], flight_details['Duration'][2*i+1]]
            print(dur_ref)
            print(time_ref)
            price = getExpFlightPrice(flight_details['Airline'][i], time_ref, dur_ref)
            price_exp_lst.append(price)

    print(price_exp_lst)


    frames_details.append(DataFrame(flight_details,
                                    columns=['Deal Index', 'Flight Leg', 'Bound', 'Departure Time', 'Arrival Time',
                                             'Duration', 'Transfer', 'Transfer Place', 'Airline']))
    df_details = pd.concat(frames_details)
    export_csv = df_details.to_csv('Skyscanner_details.csv', index=None)
    print(df_details)

    frames_main.append(DataFrame(flight_main,
                                 columns=['Deal', 'Price', 'Hyperlink']))
    df_main = pd.concat(frames_main)
    export_csv = df_main.to_csv('Skyscanner_main.csv', index=None)
    print(df_main)
