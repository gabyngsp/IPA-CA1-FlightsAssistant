import tagui as t
import tagui_util as tu, DB_Functions as dbf
from datetime import datetime as dt
from Skyscanner_getFlightInfo import getFlightExcel


def lookup_cabin_class(cabin):
    strCabin = "Economy"
    if "first" in cabin.lower():
        strCabin = "First"
    elif "business" in cabin.lower():
        strCabin = "Business"
    elif "premium" in cabin.lower():
        strCabin = "PremiumEconomy"
    else:
        strCabin = "Economy"
    return strCabin

def number_of_travellers(adult_pax, children_pax, children_age):
    print(f"Adults: {adult_pax} and Children: {children_pax}")
    form_adult_pax = int(t.read('//input[@id="search-controls-adults-nudger"]'))
    form_children_pax = int(t.read('//input[@id="search-controls-children-nudger"]'))
    print(f"Form Current Adults: {form_adult_pax} and Children: {form_children_pax}")
    # set the number of adult travellers
    if adult_pax > form_adult_pax:
        for n in range(form_adult_pax, adult_pax):
            t.click('//button[@title="Increase number of adults"]')
            t.wait(1)
    elif adult_pax < form_adult_pax:
        for x in range(0,form_adult_pax-adult_pax):
            t.click('//button[@title="Decrease number of adults"]')
            t.wait(1)
    else:
        for n in range(form_adult_pax, adult_pax):
            t.click('//button[@title="Increase number of adults"]')
            t.wait(1)

    # set the number of child travellers
    if children_pax > form_children_pax:
        for n in range(form_children_pax, children_pax):
            t.click('//button[@title="Increase number of children"]')
            t.wait(1)
    elif children_pax < form_children_pax:
        for x in range(0,form_children_pax-children_pax):
            t.click('//button[@title="Decrease number of children"]')
            t.wait(1)
    else:
        for n in range(form_children_pax,children_pax):
            t.click('//button[@title="Increase number of children"]')
            t.wait(1)

    # Set the age for each child traveller
    if len(children_age) > 0:
        for m in range(0,len(children_age)):
            t.click(f'//select[@id="children-age-dropdown-{m}"]')
            t.select(f'//select[@id="children-age-dropdown-{m}"]',str(children_age[m]))

    t.click('//section[@id="cabin-class-travellers-popover"]//button[.="Done"]')

def one_way_trip(enquiry):
    start_date = dt.strptime(enquiry["dates"][0], '%d/%m/%Y')
    start_month = start_date.strftime('%Y-%m')
    adult_pax = int(enquiry['adult'])
    child_pax = len(enquiry['child_age'])
    child_age = enquiry['child_age']
    t.click('//input[@id="fsc-trip-type-selector-one-way"]')
    t.wait(0.5)
    t.type('//input[@id="fsc-origin-search"]', enquiry["city"][0])
    t.wait(0.5)
    t.type('//input[@id="fsc-destination-search"]', enquiry["city"][1])
    t.wait(0.5)
    t.click('//button[@id="depart-fsc-datepicker-button"]//span[starts-with(@class,"DateInput")]')
    t.click(f'//select[@id="depart-calendar__bpk_calendar_nav_select"]')
    t.select('//select[@id="depart-calendar__bpk_calendar_nav_select"]', f'{start_month}')
    t.click(f'//button[starts-with(@class,"BpkCalendarDate") and contains(@aria-label,"{start_date.strftime("%d %B %Y").lstrip("0")}")]')
    t.click('//button[starts-with(@id,"CabinClassTravellersSelector")]')
    t.click('//select[@id="search-controls-cabin-class-dropdown"]')
    t.select('//select[@id="search-controls-cabin-class-dropdown"]', lookup_cabin_class(enquiry["cabin_class"]))

    # t.select('//select[@id="search-controls-cabin-class-dropdown"]',(enquiry["cabin_class"].capitalize()).replace(' ',''))
    number_of_travellers(adult_pax,child_pax,child_age)
    t.click('//button[@type="submit"][@aria-label="Search flights"]')

def return_trip(enquiry):
    start_date = dt.strptime(enquiry["dates"][0], '%d/%m/%Y')
    start_month = start_date.strftime('%Y-%m')
    end_date = dt.strptime(enquiry["dates"][1], '%d/%m/%Y')
    end_month = start_date.strftime('%Y-%m')
    adult_pax = int(enquiry['adult'])
    child_pax = len(enquiry['child_age'])
    child_age = enquiry['child_age']
    t.click('//input[@id="fsc-trip-type-selector-return"]')
    t.wait(0.5)
    t.type('//input[@id="fsc-origin-search"]', enquiry["city"][0])
    t.wait(0.5)
    t.type('//input[@id="fsc-destination-search"]', enquiry["city"][1])
    t.wait(0.5)
    t.click('//button[@id="depart-fsc-datepicker-button"]//span[starts-with(@class,"DateInput")]')
    t.click(f'//select[@id="depart-calendar__bpk_calendar_nav_select"]')
    t.select('//select[@id="depart-calendar__bpk_calendar_nav_select"]', f'{start_month}')
    t.click(f'//button[starts-with(@class,"BpkCalendarDate") and contains(@aria-label,"{start_date.strftime("%d %B %Y").lstrip("0")}")]')
    t.click('//button[@id="return-fsc-datepicker-button"]//span[starts-with(@class,"DateInput")]')
    t.click(f'//select[@id="return-calendar__bpk_calendar_nav_select"]')
    t.select('//select[@id="return-calendar__bpk_calendar_nav_select"]', f'{end_month}')
    t.click(f'//button[starts-with(@class,"BpkCalendarDate") and contains(@aria-label,"{end_date.strftime("%d %B %Y").lstrip("0")}")]')
    t.click('//button[starts-with(@id,"CabinClassTravellersSelector")]')
    t.click('//select[@id="search-controls-cabin-class-dropdown"]')
    t.select('//select[@id="search-controls-cabin-class-dropdown"]',lookup_cabin_class(enquiry["cabin_class"]))
    number_of_travellers(adult_pax,child_pax,child_age)

    t.click('//button[@type="submit" and @aria-label="Search flights"]')

def multi_city_trip(enquiry):
    t.click('//input[@id="fsc-trip-type-selector-multi-destination"]')
    travel_dates = enquiry["dates"]
    numDep = len(travel_dates)
    cities = enquiry["city"]
    numCity = len(cities)
    form_flightleg = t.count('//*[@id="flights-search-controls-root"]/div/div/form/div[2]/ol/li')
    if numDep < form_flightleg:
        for cnt in range(form_flightleg-numDep):
            t.click(f'//*[@id="flights-search-controls-root"]/div/div/form/div[2]/ol/li[{form_flightleg-cnt}]/div[4]/button')
    elif numDep > form_flightleg:
        for cnt in range(numDep-form_flightleg):
            t.click('//div[starts-with(@class,"MulticityControls_MulticityControls__add-leg-wrapper__2arYh")]/button')
            t.wait(0.5)

    for num in range(0,numDep):
        start_date = dt.strptime(travel_dates[num], '%d/%m/%Y')
        start_month = start_date.strftime('%Y-%m')
        orig_city = cities[num]
        if numCity == numDep:
            if num < numDep-1:
                dest_city = cities[num+1]
            else:
                dest_city = cities[0]
        else:
            dest_city = cities[num+1]
        t.type(f'//input[@id="fsc-origin-search-{num}"]', orig_city)
        t.wait(0.5)
        t.type(f'//input[@id="fsc-destination-search-{num}"]', dest_city)
        t.wait(0.5)
        t.click(f'//button[@id="fsc-leg-date-{num}-fsc-datepicker-button"]//span[starts-with(@class,"DateInput")]')
        t.click(f'//select[@id="fsc-leg-date-{num}-calendar__bpk_calendar_nav_select"]')
        t.select(f'//select[@id="fsc-leg-date-{num}-calendar__bpk_calendar_nav_select"]', f'{start_month}')
        t.click(f'//button[starts-with(@class,"BpkCalendarDate") and contains(@aria-label,"{start_date.strftime("%d %B %Y").lstrip("0")}")]')


    t.click('//button[starts-with(@id,"CabinClassTravellersSelector")]')
    t.click('//select[@id="search-controls-cabin-class-dropdown"]')
    t.select('//select[@id="search-controls-cabin-class-dropdown"]', lookup_cabin_class(enquiry["cabin_class"]))
    adult_pax = int(enquiry['adult'])
    child_pax = len(enquiry['child_age'])
    child_age = enquiry['child_age']
    number_of_travellers(adult_pax, child_pax, child_age)

    t.click('//button[@type="submit"][@aria-label="Search flights"]')

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

def flight_search(flight_request):
    search_dt = dt.today()
    request_id = flight_request['Request_ID']
    info = flight_request['Request_Details']
    t.init()
    t.url('https://www.skyscanner.com.sg/')
    tu.wait_for_pageload('//input[@id="fsc-trip-type-selector-return"]')
    fill_search(info)
    ind = 0
    flight_main = getFlightExcel(info,ind)
    t.wait(10.0)
    t.close()
    flight_main.update({'Request_ID': request_id,
                        'Search_Datetime':search_dt})
    dbf.newFlightDeals(flight_main)
    outFile = dbf.export_FlightDeals(request_id,search_dt)
    return outFile

