import requests
from bs4 import BeautifulSoup


CAPO_URL = 'http://www.capogirogelato.com/flavors.php'
location_numbers = {}
location_numbers['13th Street'] = '1'
location_numbers['Rittenhouse'] = '2'
location_numbers['CapoYunk'] = '3'
location_numbers['CapoPenn'] = '4'


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

def extract_flavors(location, html):
    """Takes HTML and returns dictionary flavor info"""
    flavor_info = {}

    soup = BeautifulSoup(html,'html.parser')

    flavors = soup.find_all('td','flavorbox')
    for flavor in flavors:
        flavor_name = flavor.contents[0].contents[0]
        try:
            flavor_description = flavor.contents[1].contents[0].contents[0]
        except:
            flavor_description = None
        flavor_info[flavor_name] = flavor_description

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



if __name__ == '__main__':
    pass
