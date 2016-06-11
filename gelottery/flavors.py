import requests
from bs4 import BeautifulSoup, SoupStrainer


CAPO_URL = 'http://www.capogirogelato.com/flavors.php'
location_numbers = {}
location_numbers['13th Street'] = '1'
location_numbers['Rittenhouse'] = '2'
location_numbers['CapoYunk'] = '3'
location_numbers['CapoPenn'] = '4'

def locations():
    """Print location names"""
    for location in sorted(location_numbers.keys()):
        print(location)

def get_flavor_html(location):
    """Returns a location's daily flavor list HTML."""
    if not location in location_numbers.keys():
        return None

    payload = {'location': location_numbers[location]}
    flavor_html = requests.get(CAPO_URL,params = payload)
    
    if flavor_html.status_code == 200:
        return flavor_html.text
    else:
        return None

def extract_flavors(loaction,html):
    """Takes HTML and returns dictionary flavor info"""
    flavor_info = {}
    relevant_html_tags = [
                            'flavorhead',
                            'flavorheadwhite',
                            'flavorcap',
                            'flavorcapwhite'
                        ]
    only_span = SoupStrainer('span', relevant_html_tags)
    soup = BeautifulSoup(html,'html.parser',parse_only=only_span)
    span = soup('span')
    num=0

    while num < len(span):
        if 'flavorhead' in span[num]['class']:
            flavor_name = span[num].string
            num+=1

            if 'flavorcap' in span[num]['class']:
                flavor_cap = span[num].string
                num += 1
            else:
                flavor_cap = None
        else:
            num +=1
        flavor_info[flavor_name] = flavor_cap

    return flavor_info

def get_location_flavors(location):
    """Returns a location's daily flavor list as a dict"""
    flavor_html = get_flavor_html(location)
    flavors = extract_flavors(location,flavor_html)
    return flavors

def get_daily_flavors():
    """Returns dict of locations : flavors available today."""
    daily_flavors = {}
    for location in location_numbers.keys():
        daily_flavors[location] = get_location_flavors(location)
    return daily_flavors