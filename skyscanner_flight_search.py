import tagui as t
from datetime import datetime as dt

from Skyscanner_getFlightInfo import getFlightExcel


def number_of_travellers(travellers):
    adult_pax = 0
    children_pax = 0
    if len(travellers.split(";")) == 1:
        if "Adults" in travellers :
            adult_pax = int(travellers.replace(" Adults",""))
        else:
            children_pax = int(travellers.replace(" Children",""))
    else:
        pax = travellers.split(";")
        adult_pax = int(pax[0].replace(" Adults",""))
        children_pax = int(pax[1].replace(" Children", ""))
        children_age = pax[2].split(",")

    print(f"Adults: {adult_pax} and Children: {children_pax}")
    form_adult_pax = int(t.read('//input[@id="search-controls-adults-nudger"]'))
    form_children_pax = int(t.read('//input[@id="search-controls-children-nudger"]'))
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
        for n in range(1, adult_pax):
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
        for n in range(0,children_pax):
            t.click('//button[@title="Increase number of children"]')
            t.wait(1)

    # Set the age for each child traveller
    if len(children_age) > 0:
        for m in range(0,len(children_age)):
            t.click(f'//select[@id="children-age-dropdown-{m}"]')
            t.select(f'//select[@id="children-age-dropdown-{m}"]',children_age[m])

    t.click('//section[@id="cabin-class-travellers-popover"]//button[.="Done"]')

def one_way_trip(enquiry):
    start_date = dt.strptime(enquiry["start_date"], '%d/%m/%Y')
    start_month = start_date.strftime('%Y-%m')
    end_date = dt.strptime(enquiry["end_date"], '%d/%m/%Y')
    end_month = end_date.strftime('%Y-%m')

    t.click('//input[@id="fsc-trip-type-selector-one-way"]')
    t.type('//input[@id="fsc-origin-search"]', enquiry["from"])
    t.type('//input[@id="fsc-destination-search"]', enquiry["to"])
    t.click('//button[@id="depart-fsc-datepicker-button"]//span[starts-with(@class,"DateInput")]')
    t.click(f'//select[@id="depart-calendar__bpk_calendar_nav_select"]')
    t.select('//select[@id="depart-calendar__bpk_calendar_nav_select"]', f'{start_month}')
    t.click(f'//button[starts-with(@class,"BpkCalendarDate") and contains(@aria-label,"{start_date.strftime("%d %B %Y").lstrip("0")}")]')
    t.click('//button[starts-with(@id,"CabinClassTravellersSelector")]')
    t.click('//select[@id="search-controls-cabin-class-dropdown"]')
    t.select('//select[@id="search-controls-cabin-class-dropdown"]',enquiry["cabin_class"].replace(' ',''))
    number_of_travellers(enquiry["pax"])
    t.click('//button[@type="submit"][@aria-label="Search flights"]')

def return_trip(enquiry):
    start_date = dt.strptime(enquiry["start_date"], '%d/%m/%Y')
    start_month = start_date.strftime('%Y-%m')
    end_date = dt.strptime(enquiry["end_date"], '%d/%m/%Y')
    end_month = end_date.strftime('%Y-%m')

    t.click('//input[@id="fsc-trip-type-selector-return"]')
    t.type('//input[@id="fsc-origin-search"]', enquiry["from"])
    t.type('//input[@id="fsc-destination-search"]', enquiry["to"])
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
    t.select('//select[@id="search-controls-cabin-class-dropdown"]',enquiry["cabin_class"].replace(' ',''))
    number_of_travellers(enquiry["pax"])

    t.click('//button[@type="submit"][@aria-label="Search flights"]')

def multi_city_trip(enquiry):
    t.click('//input[@id="fsc-trip-type-selector-flight-destination"]')
    print("Pending Code")

def fill_search(enquiry):
    trip_type=enquiry["trip_type"]
    # Select if looking for return / one-way / multi-city
    if '1' in trip_type: # return
        return_trip(enquiry)
    elif '2' in trip_type: # one way
        one_way_trip(enquiry)
    elif '3' in trip_type: # multi city
        multi_city_trip(enquiry)
    else:
        one_way_trip(enquiry)

def flight_search(info):
    t.init()
    t.url('https://www.skyscanner.com.sg/')
    #info = {'from': 'beijing', 'to': 'singapore', 'trip_type': '1', 'start_date': '01/11/2019','end_date': '03/11/2019', 'cabin_class': 'economy', 'pax': '2 Adults;2 Children;2,3'}
    fill_search(info)
    getFlightExcel(info)
    #t.wait(10.0)
    #t.close()


