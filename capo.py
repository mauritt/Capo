import requests
from bs4 import BeautifulSoup
from capo_locations import locations


CAPO_URL = 'http://www.capogirogelato.com/flavors.php'

def get_flavor_html(location):
    """Returns a location's daily flavor list HTML."""
    if not location in locations:
        return None

    payload = {'location': locations[location]['number']}
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

def get_location_flavor(location):
    """Returns a location's daily flavor list as a dict"""
    flavor_html = get_flavor_html(location)
    flavors = extract_flavors(location,flavor_html)
    return flavors




if __name__ == '__main__':
    pass
