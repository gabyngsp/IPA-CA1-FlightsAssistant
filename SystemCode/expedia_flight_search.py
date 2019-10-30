import tagui as t
from SystemCode import tagui_util as tu
from datetime import datetime as dt

def lookup_cabin_class(cabin):
    strCabin = "economy"
    if "first" in cabin.lower():
        strCabin = "first"
    elif "business" in cabin.lower():
        strCabin = "business"
    elif "premium" in cabin.lower():
        strCabin = "premium"
    else:
        strCabin = "economy"
    return strCabin

def child_infant_breakdown(children_age):
    get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x > y]
    infant_index = get_indexes(2,children_age)
    child_age = []
    infant_age = []
    for idx in range(0,len(children_age)):
        if idx in infant_index:
            infant_age.append(children_age[idx])
        else:
            child_age.append(children_age[idx])

    return child_age, infant_age

def number_of_travellers(adult_pax, children_pax, children_age):
    print(f"Adults: {adult_pax} and Children: {children_pax}")
    t.click(f'//select[@id="adult-count"]')
    t.select('//select[@id="adult-count"]', f'{adult_pax}')

    # set the number of child travellers
    t.click(f'//select[@id="child-count"]')
    t.select('//select[@id="child-count"]', f'{children_pax}')

    # Set the age for each child traveller
    if children_pax > 0:
        for m in range(0,children_pax):
            print(f'Child {m+1} age {str(children_age[m])}')
            t.click(f'//select[@id="child-age-{m+1}"]')
            t.wait(1)
            t.select(f'//select[@id="child-age-{m+1}"]',str(children_age[m]))
            t.wait(1)


def one_way_trip(enquiry):
    start_date = dt.strptime(enquiry["dates"][0], '%d/%m/%Y')

    t.click('//input[@id="flight-type-one-way-hp-flight"]')
    t.type('//input[@id="flight-origin-hp-flight"]', enquiry["city"][0])
    t.type('//input[@id="flight-destination-hp-flight"]', enquiry["city"][1])
    t.type('//input[@id="flight-departing-single-hp-flight"]', '[clear]')
    t.type('//input[@id="flight-departing-single-hp-flight"]', start_date.strftime("%d/%m/%Y"))
    t.click('//*[@id="traveler-selector-hp-flight"]/div/ul/li/button')
    t.click('//a[@id="flight-advanced-options-hp-flight"]')
    t.select('//select[@id="flight-advanced-preferred-class-hp-flight"]',lookup_cabin_class(enquiry["cabin_class"]))
    t.click('//*[@id="gcw-flights-form-hp-flight"]/div[8]/label/button')

def return_trip(enquiry):
    start_date = dt.strptime(enquiry["dates"][0], '%d/%m/%Y')
    end_date = dt.strptime(enquiry["dates"][1], '%d/%m/%Y')

    t.click('//input[@id="flight-type-roundtrip-hp-flight"]')
    t.type('//input[@id="flight-origin-hp-flight"]', enquiry["city"][0])
    t.type('//input[@id="flight-destination-hp-flight"]', enquiry["city"][1])
    t.type('//input[@id="flight-departing-hp-flight"]', '[clear]')
    t.type('//input[@id="flight-departing-hp-flight"]', start_date.strftime("%d/%m/%Y"))
    t.click('//*[@id="traveler-selector-hp-flight"]/div/ul/li/button')
    t.click('//a[@id="flight-advanced-options-hp-flight"]')
    t.select('//select[@id="flight-advanced-preferred-class-hp-flight"]',lookup_cabin_class(enquiry["cabin_class"]))
    t.click('//*[@id="gcw-flights-form-hp-flight"]/div[8]/label/button')
    tu.wait_for_pageload('//button[@id="flights-advanced-options-toggle"]')
    curr_enddate = t.read('//input[@id="return-date-1"]')
    if curr_enddate != end_date.strftime("%d/%m/%Y") :
        t.type('//input[@id="return-date-1"]', '[clear]')
        t.type('//input[@id="return-date-1"]', end_date.strftime("%d/%m/%Y"))
    t.click('//*[@id="flight-wizard-search-button"]')

def multi_city_trip(enquiry):
    t.click('//input[@id="flight-type-multi-dest-hp-flight"]')
    travel_dates = enquiry["dates"]
    numDep = len(travel_dates)
    cities = enquiry["city"]
    numCity = len(cities)

    form_flightleg = (t.count('//div[@class="cols-nested gcw-multidest-flights-container"]/div/fieldset'))
    print(form_flightleg)
    if numDep < form_flightleg:
        for cnt in range(form_flightleg-numDep):
            t.click(f'//*[@id="flightlegs-list-fieldset-{form_flightleg-cnt}-hp-flight"]/div/a')
    elif numDep > form_flightleg:
        for cnt in range(numDep-form_flightleg):
            t.click('//a[@id="add-flight-leg-hp-flight"]')
            t.wait(0.5)

    t.type('//input[@id="flight-origin-hp-flight"]', cities[0])
    t.type('//input[@id="flight-destination-hp-flight"]', cities[1])
    t.type('//input[@id="flight-departing-single-hp-flight"]', '[clear]')
    t.type('//input[@id="flight-departing-single-hp-flight"]', (dt.strptime(travel_dates[0], '%d/%m/%Y')).strftime("%d/%m/%Y"))

    for num in range(1,numDep):
        print(f"num:{num} and form_flightleg:{form_flightleg}")

        start_date = dt.strptime(travel_dates[num], '%d/%m/%Y')
        orig_city = cities[num]
        if numCity == numDep:
            if num < numDep-1:
                dest_city = cities[num+1]
            else:
                dest_city = cities[0]
        else:
            dest_city = cities[num+1]

        t.type(f'//input[@id="flight-{num+1}-origin-hp-flight"]', orig_city)
        t.wait(0.5)
        t.type(f'//input[@id="flight-{num+1}-destination-hp-flight"]', dest_city)
        t.wait(0.5)
        t.type(f'//input[@id="flight-{num+1}-departing-hp-flight"]', '[clear]')
        t.type(f'//input[@id="flight-{num+1}-departing-hp-flight"]', start_date.strftime("%d/%m/%Y"))

    t.click('//a[@id="flight-advanced-options-hp-flight"]')
    t.select('//select[@id="flight-advanced-preferred-class-hp-flight"]',lookup_cabin_class(enquiry["cabin_class"]))
    t.click('//*[@id="gcw-flights-form-hp-flight"]/div[8]/label/button')

def fill_search(enquiry):
    # Select if looking for return / one-way / multi-city
    if len(enquiry["dates"]) == 1: # one way
        print("one way trip")
        one_way_trip(enquiry)
    elif len(enquiry["dates"]) == 2:
        if len(enquiry["city"]) > 2: # return
            print("multi-city trip")
            multi_city_trip(enquiry)
        else:                        # return
            print("return trip")
            return_trip(enquiry)
    elif len(enquiry["dates"]) > 2: # multi city
        print("multi-city trip")
        multi_city_trip(enquiry)
    else:
        one_way_trip(enquiry)


def flight_search(info):
    t.url('https://www.expedia.com.sg/')
    tu.wait_for_pageload('//button[@id="tab-flight-tab-hp"]')
    t.click('//button[@id="tab-flight-tab-hp"]')
    fill_search(info)
    tu.wait_for_pageload('//button[@id="flights-advanced-options-toggle"]')
    t.click('//button[@id="flights-advanced-options-toggle"]')
    tu.wait_for_pageload('//select[@id="child-count"]')
    adult_pax = int(info['adult'])
    children_pax = len(info['child_age'])
    children_age = info['child_age']
    number_of_travellers(adult_pax, children_pax, children_age)
    t.click('//*[@id="flight-wizard-search-button"]')

