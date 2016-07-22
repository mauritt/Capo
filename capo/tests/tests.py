import sys
import unittest
import requests
from io import StringIO
from unittest import mock
import flavors


class FlavorTest(unittest.TestCase):

    @mock.patch('sys.stdout',new_callable=StringIO)
    def test_locations(self, mock_stdout):
        print_test = '13th Street\nCapoPenn\nCapoYunk\nRittenhouse\n'
        flavors.locations()
        self.assertEqual(mock_stdout.getvalue(),print_test)

    def test_get_flavor_html(self):
        with mock.patch('requests.get') as get:
            URL = 'http://www.capogirogelato.com/flavors.php'
            payload = {'location':'1'}
            MockResponse = mock.Mock()
            MockResponse.status_code = 200
            MockResponse.text = "It worked!"
            get.return_value = MockResponse
            self.assertEqual(flavors.get_flavor_html('13th Street'),'It worked!')
            get.assert_called_with(URL, params = payload)

    def test_extract_flavors(self):
                expected_flavors = {
                "Pompelmo Rosso con Campari": 
                    "Ruby Red Grapefruit with Campari",
                "Fico D'India (Red)":
                    "Cactus or prickly pears.  Tastes like a watermelon.",
                "Stracciatella": 
                    "Fior di latte with slivers of dark chocolate.",
                "Fior Di Latte": 
                    "Milk gelato.  Milk from an Amish family's single herd of hormone free, grass fed in Lancaster County.  Crazy good.",
                "Carambola con Limone Verde":
                    "Carambola (Star Fruit) with tart limes.",
                "Pistacchio Siciliano":
                    "The very best pistacchios from Sicily.  Not that horrific neon green kind, the amazing olive green kind.",
                "Cioccolato Scuro": 
                    "Rich, black and serious.",
                "Mora Gelato": 
                    "Lancaster County Blackberries.",
                "Dulce De Leche": 
                    "Our own decadent Argentine caramel swirled into Fior di Latte gelato.",
                "Nocciola Piemontese": 
                    "Hazelnut gelato made with nuts from the Piedmont region of Italy.  When this is your first choice, you have your Italian Citizenship.",
                "Lemon": 
                    "Classic lemon sorbetto.  Tart and refreshing.",
                "Banana": 
                    None,
                "Thai Coconut Milk":
                    "Sweet smooth coconut gelato made with coconut milk from Thailand and a hint of coconut rum.",
                "Uva Rossa":
                    "Tart red grapes.",
                "Peanut Butter":
                    "Peanut gelato layered with house roasted peanut butter.",
                "Cappuccino": 
                    "Made with La Colombe coffee.  Only the best.",
                "Bacio": 
                    None,
                "Pecan": 
                    "Pecans from Geogia.",
                "Lime with Cilantro": 
                    "Tart limes with the interesting herb, cilantro.  Our cilantro is from Landsdale, PA.",
                "White Chocolate": 
                    "Valhrona white chocolate.",
                }

                with open('tests/mocks/mock_flavors.html','r') as mock_html:

                    flavor_info = flavors.extract_flavors(mock_html.read())
                    for name,caption in expected_flavors.items():
                        self.assertEqual(expected_flavors[name],flavor_info[name])


    def test_get_location_flavors(self):
        with mock.patch('flavors.get_flavor_html') as get_flavor_html:
            get_flavor_html.return_value = '<html>Test</html>'
            
            with mock.patch('flavors.extract_flavors') as extract_flavors:
                extract_flavors.return_value = {'name':'description'}
                location_flavors = flavors.get_location_flavors('13th Street')
                self.assertEqual(location_flavors,{'name':'description'})
                get_flavor_html.assert_called_with('13th Street')
                extract_flavors.assert_called_with('<html>Test</html>')

    def test_get_daily_flavors(self):
        locations = ['13th Street', 'CapoPenn','CapoYunk','Rittenhouse']
        test_dict = {}
        calls = []
        
        for location in locations:
            test_dict[location] = {'name':'description'}
            calls.append(mock.call(location))
        
        with mock.patch('flavors.get_location_flavors') as get_location_flavors:
            get_location_flavors.return_value = {'name':'description'}


            flavors_today = flavors.get_daily_flavors()
            self.assertEqual(flavors_today,test_dict)
            get_location_flavors.assert_has_calls(calls)









