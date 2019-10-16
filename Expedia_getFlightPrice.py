import tagui as t
import tagui_util as util



def getExpFlightPrice(airline, dep_ref, dur_ref):
    t.url(
        'https://www.expedia.com.sg/Flights-Search?flight-type=on&starDate=18%2F10%2F2019&endDate=23%2F10%2F2019&mode=search&trip=roundtrip&leg1=from%3Asingapore%2Cto%3Abeijing%2Cdeparture%3A18%2F10%2F2019TANYT&leg2=from%3Abeijing%2Cto%3Asingapore%2Cdeparture%3A23%2F10%2F2019TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY')
    t.wait(5)
    util.wait_for_pageload('//input[@classes="filter-checkbox"]')
    airline = airline.replace(' ', '-')+'-Airlines'
    t.click(f'//span[@id="{airline}-flights-checkbox"]')

    for i in range(len(dep_ref)):
        if dep_ref[i][0] == '0':
            print('0')
            dep_ref[i] = dep_ref[i][1:]
        dur_ref[i] = dur_ref[i] + 'm'


    print(airline)
    print(dep_ref)
    print(dur_ref)

    util.wait_for_pageload('//button[@data-test-id="select-button"]')
    t.wait(5)
    for i in range(t.count(f'//ul[@id="flightModuleList"]//li') - 1):
        i = i + 1
        dep = util.hover_and_read(f'(//span[@data-test-id="departure-time"])[{i}]')
        print('time ',dep)
        print('ref ', dep_ref[0])
        if dep == dep_ref[0]:
            print('dep OK')
            dur = util.hover_and_read(f'(//span[@data-test-id="duration"])[{i}]')
            if dur == dur_ref[0]:
                print(i)
                price_org = util.hover_and_read(f'(//span[@data-test-id="listing-price-dollars"])[{i}]')
                if len(dur_ref) == 1:
                    return price
                elif len(dur_ref) == 2:
                    t.click(f'(//button[@data-test-id="select-button"])[{i}]')

                    util.wait_for_pageload('//button[@data-test-id="select-button"]')
                    print('OK')
                    for j in range(t.count(f'//ul[@id="flightModuleList"]//li') - 1):
                        j = j + 1
                        print(j)
                        dep = util.hover_and_read(f'(//span[@data-test-id="departure-time"])[{j}]')
                        if dep == dep_ref[1]:
                            dur = util.hover_and_read(f'(//span[@data-test-id="duration"])[{j}]')
                            if dur == dur_ref[1]:
                                price_plus = util.hover_and_read(
                                    f'(//span[@data-test-id="listing-price-dollars"])[{j}]')
                                price = int(price_org[3:]) + int(price_plus[5:])
                                return price


