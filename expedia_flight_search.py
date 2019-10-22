import tagui as t
import tagui_util as tu
from datetime import datetime as dt


#one way
#info = {'city': ['singapore','beijing'], 'trip_type': '', 'dates': ['01/11/2019'], 'cabin_class': 'economy', 'adult': '2', 'child_age': [3,1]}
# #return
#info = {'city': ['singapore','beijing'], 'trip_type': '', 'dates': ['01/11/2019','05/11/2019'], 'cabin_class': 'economy', 'adult': '2', 'child_age': [1,3]}
# #multi-city
#info = {'city': ['singapore','beijing','tokyo'], 'trip_type': '', 'dates': ['01/11/2019','05/11/2019','10/11/2019'], 'cabin_class': 'economy', 'adult': '2', 'child_age': [3,10]}

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
    t.click('//*[@id="gcw-flights-form-hp-flight"]/div[8]/label/button')

def return_trip(enquiry):
    start_date = dt.strptime(enquiry["dates"][0], '%d/%m/%Y')
    end_date = dt.strptime(enquiry["dates"][1], '%d/%m/%Y')

    t.click('//input[@id="flight-type-roundtrip-hp-flight"]')
    t.type('//input[@id="flight-origin-hp-flight"]', enquiry["city"][0])
    t.type('//input[@id="flight-destination-hp-flight"]', enquiry["city"][1])
    t.type('//input[@id="flight-departing-hp-flight"]', '[clear]')
    t.type('//input[@id="flight-departing-hp-flight"]', start_date.strftime("%d/%m/%Y"))
    t.type('//input[@id="flight-returning-hp-flight"]', '[clear]')
    t.type('//input[@id="flight-returning-hp-flight"]', end_date.strftime("%d/%m/%Y"))
    t.click('//*[@id="traveler-selector-hp-flight"]/div/ul/li/button')
    t.click('//*[@id="gcw-flights-form-hp-flight"]/div[8]/label/button')

def multi_city_trip(enquiry):
    t.click('//input[@id="flight-type-multi-dest-hp-flight"]')
    travel_dates = enquiry["dates"]
    numDep = len(travel_dates)
    cities = enquiry["city"]
    form_flightleg = (t.count('//div[@class="cols-nested gcw-multidest-flights-container"]/div/fieldset'))
    print(form_flightleg)
    t.type('//input[@id="flight-origin-hp-flight"]', cities[0])
    t.type('//input[@id="flight-destination-hp-flight"]', cities[1])
    t.type('//input[@id="flight-departing-single-hp-flight"]', '[clear]')
    t.type('//input[@id="flight-departing-single-hp-flight"]', (dt.strptime(travel_dates[0], '%d/%m/%Y')).strftime("%d/%m/%Y"))

    for num in range(1,numDep):
        #add new flight leg
        print(f"num:{num} and form_flightleg:{form_flightleg}")
        if num >= 2 and num >= form_flightleg:
            t.click('//a[@id="add-flight-leg-hp-flight"]')
            t.wait(0.5)

        start_date = dt.strptime(travel_dates[num], '%d/%m/%Y')
        orig_city = cities[num]
        if num < numDep-1:
            dest_city = cities[num+1]
        else:
            dest_city = cities[0]
        t.type(f'//input[@id="flight-{num+1}-origin-hp-flight"]', orig_city)
        t.wait(0.5)
        t.type(f'//input[@id="flight-{num+1}-destination-hp-flight"]', dest_city)
        t.wait(0.5)
        t.type(f'//input[@id="flight-{num+1}-departing-hp-flight"]', '[clear]')
        t.type(f'//input[@id="flight-{num+1}-departing-hp-flight"]', start_date.strftime("%d/%m/%Y"))

    t.click('//*[@id="gcw-flights-form-hp-flight"]/div[8]/label/button')

def fill_search(enquiry):
    # Select if looking for return / one-way / multi-city
    if len(enquiry["dates"]) == 1: # one way
        print("one way trip")
        one_way_trip(enquiry)
    elif len(enquiry["dates"]) == 2: # return
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

##t.init()
#t.wait(0.5)
#flight_search(info)
# t.wait(10)
# t.close()