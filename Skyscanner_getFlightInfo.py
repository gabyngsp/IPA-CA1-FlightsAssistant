import pandas as pd
import tagui as t
import tagui_util as util
from pandas import DataFrame

#dep = 'dlc'
#arr = 'sins'
#date_dep = ['191013', '191014']
#date_arr = '191020/'
#date_arr = ''
#adults = '2'
#children = '2'
#adultsv2 = '1'
#childrenv2 = ''
#cabinclass = 'economy'

#def getFlightInfo(dep, arr, date_dep, date_arr, adults, children, adultsv2, childrenv2, cabinclass):
def getFlightInfo(info):
    #url = 'https://www.skyscanner.com.sg/transport/flights/' + info['dep'] + '/' + info['arr'] + '/' + info['start_date'] + '/' + info['end_date'] + '?adults=' + adults + '&children=' + children + '&adultsv2=' + adultsv2 + '&childrenv2=' + childrenv2 + '&infants=0&cabinclass=' + info['cabin_class'] + '&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home'
    util.wait_for_pageload(
        '//div[@class="ResultsSummary_summaryContainer__3_ZX_"]//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT SummaryInfo_itineraryCountContainer__30Hjd"]')
    time_dep_lst = []
    time_arr_lst = []
    time_arr_day_lst = []
    airline_lst = []
    dur_lst = []
    time_dep_rt_lst = []
    time_arr_rt_lst = []
    time_arr_day_rt_lst = []
    airline_rt_lst = []
    dur_rt_lst = []
    transfer_rt_lst = []
    transfer_plc_rt_lst = []
    price_lst = []
    transfer_lst = []
    transfer_plc_lst = []
    href_lst = []
    date_lst = []
    date_rt_lst = []
    m = 1
    for n in range(2):
        if t.present('//span[@class="BpkBadge_bpk-badge__2mEjm "]'):
            k = n + 1
        else:
            k = n
        href = util.hover_and_read(f'(//a[@class="FlightsTicket_link__kl4DL"])[{n + 1}]//@href')
        price = util.hover_and_read(
            f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN BpkText_bpk-text--bold__4yauk"])[{k + 4}]')

        if '2' in info["trip_type"]: # one way
            print('single')
            time_dep = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN"])[{2 * n + 1}]')
            time_arr = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN"])[{2 * n + 2}]')
            airline = util.hover_and_read(f'(//img[@class="BpkImage_bpk-image__img__3HwXN"])[{2 * k + 1}]/@alt')
            dur = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT Duration_duration__1QA_S"])[{n + 1}]')
            transfer = util.hover_and_read(f'(//div[@class="LegInfo_stopsLabelContainer__2dEdt"]/span)[{n + 1}]')
            if transfer == 'Direct':
                transfer_plc = ''
            elif transfer == '1 stop':
                transfer_plc = util.hover_and_read(
                    f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT LegInfo_stopStation__Ec5OU"])[{m}]')
                m = m + 1
            if t.present(
                    '(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN LegInfo_routePartialTime__2HfzB"])[' + str(
                        2 * n + 2) + ']//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT TimeWithOffsetTooltip_offsetTooltip__24Ffv"]'):
                time_arr_day = util.hover_and_read(
                    f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN LegInfo_routePartialTime__2HfzB"])[{2 * n + 2}]//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT TimeWithOffsetTooltip_offsetTooltip__24Ffv"]')
            else:
                time_arr_day = ''
        else:
            print('return')
            time_dep = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN"])[{4 * n + 1}]')
            time_arr = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN"])[{4 * n + 2}]')
            time_dep_rt = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN"])[{4 * n + 3}]')
            time_arr_rt = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN"])[{4 * n + 4}]')
            print(time_dep_rt)
            airline = util.hover_and_read(f'(//img[@class="BpkImage_bpk-image__img__3HwXN"])[{3 * n + 2}]/@alt')
            airline_rt = util.hover_and_read(f'(//img[@class="BpkImage_bpk-image__img__3HwXN"])[{3 * n + 3}]/@alt')
            print(airline_rt)

            dur = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT Duration_duration__1QA_S"])[{2*n + 1}]')
            print(dur)
            dur_rt = util.hover_and_read(
                f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT Duration_duration__1QA_S"])[{2*n + 2}]')
            print(dur_rt)
            transfer = util.hover_and_read(f'(//div[@class="LegInfo_stopsLabelContainer__2dEdt"]/span)[{2*n + 1}]')
            transfer_rt = util.hover_and_read(f'(//div[@class="LegInfo_stopsLabelContainer__2dEdt"]/span)[{2*n + 1}]')
            print(transfer)
            print(transfer_rt)
            if transfer == 'Direct':
                transfer_plc = ''
            elif transfer == '1 stop':
                transfer_plc = util.hover_and_read(
                    f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT LegInfo_stopStation__Ec5OU"])[{m}]')
                m = m + 1
            print(transfer_plc)

            if transfer_rt == 'Direct':
                transfer_plc_rt = ''
            elif transfer_rt == '1 stop':
                transfer_plc_rt = util.hover_and_read(
                    f'(//span[@class="BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT LegInfo_stopStation__Ec5OU"])[{m}]')
                m = m + 1
            print(transfer_plc_rt)

        time_arr_day_rt = ''
        time_arr_day = ''
        href_lst.append(t.url()[0:-2] + href)
        time_dep_lst.append(time_dep)
        time_arr_lst.append(time_arr)
        airline_lst.append(airline)
        dur_lst.append(dur)
        price_lst.append(price)
        time_arr_day_lst.append(time_arr_day)
        transfer_lst.append(transfer)
        transfer_plc_lst.append(transfer_plc)
        date_lst.append(info['start_date'])

        time_dep_rt_lst.append(time_dep_rt)
        time_arr_rt_lst.append(time_arr_rt)
        time_arr_day_rt_lst.append(time_arr_day_rt)
        airline_rt_lst.append(airline_rt)
        dur_rt_lst.append(dur_rt)
        transfer_rt_lst.append(transfer_rt)
        transfer_plc_rt_lst.append(transfer_plc_rt)
        date_rt_lst.append(info['end_date'])

        flight = {'date_lst': date_lst, 'time_dep': time_dep_lst, 'time_arr': time_arr_lst, 'airline_lst': airline_lst,
                  'dur_lst': dur_lst, 'time_arr_day_lst': time_arr_day_lst, 'transfer_lst': transfer_lst, 'transfer_plc_lst': transfer_plc_lst,
                  'date_rt_lst': date_rt_lst, 'time_dep_rt_lst': time_dep_rt_lst, 'time_arr_rt_lst': time_arr_rt_lst,
                  'airline_rt_lst': airline_rt_lst, 'dur_rt_lst': dur_rt_lst, 'time_arr_day_rt_lst': time_arr_day_rt_lst, 'transfer_rt_lst': transfer_rt_lst,
                  'transfer_plc_rt_lst': transfer_plc_rt_lst, 'price_lst': price_lst, 'href_lst': href_lst}
    return flight

def getFlightExcel(info):
    frames = []
    for i in range(len(info['start_date'])):
        flight_info = getFlightInfo(info)

        frames.append(DataFrame(flight_info, columns=['date_lst', 'time_dep', 'time_arr', 'airline_lst',
                                                  'dur_lst', 'time_arr_day_lst', 'transfer_lst', 'transfer_plc_lst',
                                                  'date_rt_lst', 'time_dep_rt_lst', 'time_arr_rt_lst',
                                                  'airline_rt_lst', 'dur_rt_lst', 'time_arr_day_rt_lst', 'transfer_rt_lst',
                                                  'transfer_plc_rt_lst', 'price_lst', 'href_lst']))

    df = pd.concat(frames)

    export_csv = df.to_csv('Skyscanner.csv', index=None)
    print(df)


#info = {'start_date':'20191101','end_date':'20191103','trip_type':'1'}
#url = 'https://www.skyscanner.com.sg/transport/flights/sins/pek/191101/191103/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home'
#getFlightExcel(info,url)