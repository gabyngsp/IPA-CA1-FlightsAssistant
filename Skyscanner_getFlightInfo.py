import pandas as pd
import tagui as t
import tagui_util as util
from pandas import DataFrame
from datetime import datetime, timedelta
from Expedia_getFlightPrice import getExpFlightPrice
from expedia_flight_search import flight_search

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
    code_lst = []
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

        q = 1
        for i in range(type):
            leg = i+1
            print(leg)

            code = util.hover_and_read(
                f'(//img[@class="BpkImage_bpk-image__img__3HwXN"]/@src)[{q}]')
            airline = util.hover_and_read(
                f'(//img[@class="BpkImage_bpk-image__img__3HwXN"])[{q}]/@alt')
            if code[37:42] != 'small':
                q = q + 1
                code = util.hover_and_read(f'(//img[@class="BpkImage_bpk-image__img__3HwXN"]/@src)[{q}]')
                airline = util.hover_and_read(
                    f'(//img[@class="BpkImage_bpk-image__img__3HwXN"])[{q}]/@alt')
                if code[37:42] != 'small':
                    q = q + 1
                    code = util.hover_and_read(f'(//img[@class="BpkImage_bpk-image__img__3HwXN"]/@src)[{q}]')
                    airline = util.hover_and_read(
                        f'(//img[@class="BpkImage_bpk-image__img__3HwXN"])[{q}]/@alt')
                    if code[37:42] != 'small':
                        q = q + 1
                        code = util.hover_and_read(f'(//img[@class="BpkImage_bpk-image__img__3HwXN"]/@src)[{q}]')
                        airline = util.hover_and_read(
                            f'(//img[@class="BpkImage_bpk-image__img__3HwXN"])[{q}]/@alt')

            q = q + 1

            print(code)
            print(airline)
            code_lst.append(code[43:45])
            print(code_lst)
            time_dep = util.hover_and_read(f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN"])[{2* type * n + 1 + 2 * i}]')
            time_arr = util.hover_and_read(f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN"])[{2* type * n + 2 + 2 * i}]')
            dur = util.hover_and_read(f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT Duration_duration__1QA_S"])[{type * n + 1 + i}]')
            transfer = util.hover_and_read(f'(//div[@class="LegInfo_stopsLabelContainer__2dEdt"]/span)[{type * n + 1 + i}]')
            print(transfer)
            if transfer == 'Direct':
                transfer_plc = ''
            elif transfer == '1 stop':
                transfer_plc = util.hover_and_read(f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT LegInfo_stopStation__Ec5OU"])[{m}]')
                m = m + 1
            print(transfer_plc)
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
        price_lst.append(int(price[1:]))
        print(price_lst)
        deal_lst.append(ind)

    details = {'Deal Index': index_lst, 'Flight Leg': leg_lst, 'Bound': bound_lst, 'Departure Time': time_dep_lst,
                   'Arrival Time': time_arr_lst, 'Duration': dur_lst, 'Transfer': transfer_lst,
                   'Transfer Place': transfer_plc_lst, 'Airline': airline_lst}
    main = {'Deal': deal_lst, 'Price': price_lst, 'Hyperlink': href_lst, 'Details': details}
    return main, time_lst, code_lst, dur_lst, ind


def getFlightExcel(info,ind):
    frames_main = []
    frames_details = []
    flight_main, time_lst, code_lst, dur_lst, ind = getFlightInfo(info['dates'], ind)

    ###Compare Price with Expedia (Hyperlink/Multi to be added)
    for i in range(2):
        t.close()
        t.init()
        t.wait(0.5)
        flight_search(info)
        t.wait(5)

        k = len(info['dates'])
        price_exp, url_exp = getExpFlightPrice(code_lst[k*i:k*(i+1)], time_lst[k*i:k*(i+1)], dur_lst[k*i:k*(i+1)])
        print(price_exp)
        print(url_exp)
        print(flight_main['Price'])
        if price_exp < flight_main['Price'][i] & price_exp != 0:
            flight_main['Price'][i] = price_exp
            flight_main['Hyperlink'][i] = url_exp
        print(flight_main['Price'])
        print(flight_main['Details']['Airline'])


