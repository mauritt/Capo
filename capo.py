import requests
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