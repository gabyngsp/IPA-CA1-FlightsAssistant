import tagui as t
import tagui_util as util



def getExpFlightPrice(airline, dep_ref, dur_ref):
    util.wait_for_pageload('//input[@classes="filter-checkbox"]')
    t.click(f'//a[@data-content-id="airlineToggleContainer"]')
    t.wait(1)
    t.click(f'//input[@id="airlineRowContainer_{airline[0]}"]')

    for i in range(len(dep_ref)):
        if dep_ref[i][0] == '0':
            dep_ref[i] = dep_ref[i][1:]

        if dur_ref[i][-1:] == 'h':
            dur_ref[i] = dur_ref[i] + ' 0m'
        else:
            dur_ref[i] = dur_ref[i] + 'm'


    print(airline)
    print(dep_ref)
    print(dur_ref)

    util.wait_for_pageload('//button[@data-test-id="select-button"]')
    t.wait(5)
    for i in range(t.count(f'//ul[@id="flightModuleList"]//li')):
        i = i + 1
        print(i)
        dep = util.hover_and_read(f'(//span[@class="medium-bold"]//span[@data-test-id="departure-time"])[{i}]')
        if len(dur_ref) == 1:
            if dep == dep_ref[0]:
                print('dep OK')
                dur = util.hover_and_read(f'(//span[@data-test-id="duration"])[{i}]')
                price_org = util.hover_and_read(f'(//span[@data-test-id="listing-price-dollars"])[{i}]')
                print(price_org)
                price = int(price_org[3:].replace(',', ''))
                print(price)
                print(type(price))
                url = t.url()
                print(url)
                return price, url

        elif len(dur_ref) == 2:
            print('trip', len(dur_ref))
            if dep == dep_ref[0]:
                print('dep OK')
                dur = util.hover_and_read(f'(//span[@data-test-id="duration"])[{i}]')
                price_org = util.hover_and_read(f'(//span[@data-test-id="listing-price-dollars"])[{i}]')
                print(price_org)
                price = int(price_org[3:].replace(',', ''))
                print(price)
                print(type(price))

                t.click(f'(//button[@data-test-id="select-button"])[{i}]')
                t.wait(5)

                util.wait_for_pageload('//button[@data-test-id="select-button"]')
                t.click(f'//input[@id="airlineRowContainer_{airline[1]}"]')
                t.wait(2)
                for j in range(t.count(f'//ul[@id="flightModuleList"]//li')):
                    j = j + 1
                    print(j)
                    dep = util.hover_and_read(f'(//span[@data-test-id="departure-time"])[{j}+1]')
                    if dep == dep_ref[1]:
                        print('return dep ok')
                        dur = util.hover_and_read(f'(//span[@data-test-id="duration"])[{j}+1]')

                        if dur == dur_ref[1]:
                            print('return dur ok')
                            price_plus = util.hover_and_read(
                                f'(//span[@data-test-id="listing-price-dollars"])[{j}]')
                            print(price_plus)
                            price = price + int(price_plus[5:])
                            print(price)
                            url = t.url()
                            print(url)
                            return price, url
        elif len(dur_ref) >= 3:
            dep_lst = []
            dur_lst = []
            print('multi-trip ', len(dur_ref))
            for k in range(len(dur_ref)):
                dep_lst.append(util.hover_and_read(f'(//span[@data-test-id="departure-time"])[{3*i+k+1}]'))
                dur_lst.append(util.hover_and_read(f'(//span[@data-test-id="duration"])[{3*i+k+1}]'))
            print(dep_lst)
            print(dep_ref)
            if dep_lst == dep_ref:
                print(dur_lst)
                print(dur_ref)
                if dur_lst == dur_ref:
                    price_org = util.hover_and_read(f'(//span[@data-test-id="listing-price-dollars"])[{i}]')
                    price = int(price_org[3:].replace(',', ''))
                    print(price)
                    #t.click(f'(//button[@data-test-id="select-button"])[{i}]')
                    url = t.url()
                    print(url)
                    return price, url



        # t.click(f'(//button[@data-test-id="select-button"])[{i}]')
        # t.wait(5)
        # if t.present('//a[@id="forcedChoiceNoThanks"]'):
        #    t.click(f'//a[@id="forcedChoiceNoThanks"]')
        # t.wait(5)
        # t.click(f'( //span[@class="packagePriceTotal"])[2]')


#one way
#info = {'city': ['singapore','beijing'], 'trip_type': '', 'dates': ['01/11/2019'], 'cabin_class': 'economy', 'adult': '2', 'child_age': [3,1]}
# #return
#info = {'city': ['singapore','beijing'], 'trip_type': '', 'dates': ['01/11/2019','05/11/2019'], 'cabin_class': 'economy', 'adult': '2', 'child_age': [1,3]}
# #multi-city
#info = {'city': ['singapore','beijing','tokyo'], 'trip_type': '', 'dates': ['01/11/2019','05/11/2019','10/11/2019'], 'cabin_class': 'economy', 'adult': '2', 'child_age': [3,10]}

#t.close()
#t.init()
#t.wait(0.5)
#flight_search(info)
#t.wait(5)
#getExpFlightPrice(['CZ', 'CZ'], ['08:05', '17:30'], ['8h 50', '9h 35'])
#getExpFlightPrice(['CZ'], ['08:05'], ['8h 50'])