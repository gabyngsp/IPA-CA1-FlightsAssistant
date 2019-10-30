import tagui as t
import tagui_util as util


def getExpFlightPrice(airline, dep_ref, dur_ref):
    print(airline)
    print(dep_ref)
    print(dur_ref)
    util.wait_for_pageload('//input[@classes="filter-checkbox"]')

    t.wait(3)
    t.click(f'//a[@data-content-id="airlineToggleContainer"]')

    for i in range(len(dep_ref)):
        if i == 0:
            if t.present(f'//input[@id="airlineRowContainer_{airline[i]}"]'):
                t.wait(3)
                t.click(f'//input[@id="airlineRowContainer_{airline[i]}"]')
            else:
                print('Not match')
                return 0, ''

        elif airline[i] != airline[i-1]:
            if t.present(f'//input[@id="airlineRowContainer_{airline[i]}"]'):
                t.wait(1)
                t.click(f'//input[@id="airlineRowContainer_{airline[i]}"]')
            else:
                print('Not match')
                return 0, ''

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
        dep = t.read(f'(//span[@class="medium-bold"]//span[@data-test-id="departure-time"])[{i}]')
        if len(dur_ref) == 1:
            if dep == dep_ref[0]:
                print('dep OK')
                dur = t.read(f'(//span[@data-test-id="duration"])[{i}]')
                t.click(f'(//button[@data-test-id="select-button"])[{i}]')
                t.wait(5)
                if t.present('//a[@id="forcedChoiceNoThanks"]'):
                    t.click(f'//a[@id="forcedChoiceNoThanks"]')
                t.wait(5)
                for x in range(5):
                    print(x)
                    if t.popup('Flight-Information?'):
                        break
                    else:
                        t.wait(5)
                price = t.read(f'(//span[@class="packagePriceTotal"])[2]')
                price = float(price.replace(',', '').replace('SG', '').replace('$', '').replace(' ', ''))
                print(price)
                url = t.url()
                return price, url
            else:
                return 0, ''

        elif len(dur_ref) == 2:
            print('trip', len(dur_ref))
            if dep == dep_ref[0]:
                print('dep OK')
                dur = t.read(f'(//span[@data-test-id="duration"])[{i}]')

                t.click(f'(//button[@data-test-id="select-button"])[{i}]')
                t.wait(5)

                util.wait_for_pageload('//button[@data-test-id="select-button"]')
                t.click(f'//input[@id="airlineRowContainer_{airline[1]}"]')
                t.wait(2)
                for j in range(t.count(f'//ul[@id="flightModuleList"]//li')):
                    j = j + 1
                    print(j)
                    dep = t.read(f'(//span[@data-test-id="departure-time"])[{j}+1]')
                    if dep == dep_ref[1]:
                        print('return dep ok')
                        dur = t.read(f'(//span[@data-test-id="duration"])[{j}+1]')

                        if dur == dur_ref[1]:
                            t.click(f'(//button[@data-test-id="select-button"])[{j}]')
                            t.wait(5)
                            if t.present('//a[@id="forcedChoiceNoThanks"]'):
                                t.click(f'//a[@id="forcedChoiceNoThanks"]')
                            t.wait(5)
                            for x in range(5):
                                print(x)
                                if t.popup('Flight-Information?'):
                                    break
                                else:
                                    t.wait(5)
                            util.wait_for_pageload('//h1[@class="section-header-main"]')
                            price = t.read(f'(//span[@class="packagePriceTotal"])[2]')
                            price = float(price.replace(',', '').replace('SG', '').replace('$', '').replace(' ', ''))
                            print(price)
                            url = t.url()
                            print(url)
                            return price, url
            else:
                return 0, ''

        elif len(dur_ref) >= 3:
            dep_lst = []
            dur_lst = []
            print('multi-trip ', len(dur_ref))
            for k in range(len(dur_ref)):
                dep_lst.append(t.read(f'(//span[@data-test-id="departure-time"])[{3*i+k+1}]'))
                dur_lst.append(t.read(f'(//span[@data-test-id="duration"])[{3*i+k+1}]'))
            print(dep_lst)
            print(dep_ref)
            if dep_lst == dep_ref:
                print(dur_lst)
                print(dur_ref)
                if dur_lst == dur_ref:
                    t.click(f'(//button[@data-test-id="select-button"])[{j}]')
                    t.wait(5)
                    if t.present('//a[@id="forcedChoiceNoThanks"]'):
                        t.click(f'//a[@id="forcedChoiceNoThanks"]')
                    t.wait(5)
                    for x in range(5):
                        print(x)
                        if t.popup('Flight-Information?'):
                            break
                        else:
                            t.wait(5)
                    price = t.read(f'(//span[@class="packagePriceTotal"])[2]')
                    price = float(price.replace(',', '').replace('SG', '').replace('$', '').replace(' ', ''))
                    print(price)
                    url = t.url()
                    print(url)
                    return price, url
            else:
                return 0, ''
