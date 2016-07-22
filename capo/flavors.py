import requests
import re

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

def extract_flavors(html):
    """Takes HTML and returns dictionary flavor info"""
    
    html = html.split('\n')

    flavor_info = {}

    span_pattern = r'<span class="%s\w*">([^>]+)</span>'

    for line in html:
        flavor_name_search = re.search(span_pattern % 'flavorhead', line)
        
        if flavor_name_search:

            flavor_name = flavor_name_search.group(1)
            flavor_caption_search = re.search(span_pattern % 'flavorcap', line)

            if flavor_caption_search:
                flavor_cap = flavor_caption_search.group(1)
            else:
                flavor_cap = None

            flavor_info[flavor_name] = flavor_cap

        else:
            pass

    return flavor_info

def get_location_flavors(location):
    """Returns a location's daily flavor list as a dict"""
    flavor_html = get_flavor_html(location)
    flavors = extract_flavors(flavor_html)
    return flavors

def get_daily_flavors():
    """Returns dict of locations : flavors available today."""
    daily_flavors = {}
    for location in sorted(location_numbers.keys()):
        daily_flavors[location] = get_location_flavors(location)
    return daily_flavors

print(get_daily_flavors())

