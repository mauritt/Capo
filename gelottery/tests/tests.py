import sys
import unittest
import requests
from io import StringIO
from unittest import mock
import flavors

class mock_soup():

    def __init__(self, span_class):
        self.span_class = span_class

    @property
    def string(self):
        if 'flavorhead' in self.span_class:
            return 'Name'
        else:
            return 'Description'
    
    def __getitem__(self,x):
        return self.span_class    



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
        mock_flavors = [
                        mock_soup('flavorhead'),
                        mock_soup('flavorcap'),
                        mock_soup('flavorheadwhite'),
                        mock_soup('flavorcapwhite'),
                        mock_soup('flavorhead'),
                        mock_soup('flavorheadwhite'),
                        mock_soup('flavorcapwhite'),
                        mock_soup('flavorheadwhite'),
                        mock_soup('flavorhead'),
                        mock_soup('flavorcap'),
                        mock_soup('flavorhead'),
        ]

        mock_html = '<html>Test</html>'

        expected_flavors = {
                              'Name': 'Description',
                              'Name': 'Description',
                              'Name': None,
                              'Name': 'Description',
                              'Name': None,
                              'Name': 'Description',
                              'Name': None
        }

        with mock.patch('flavors.SoupStrainer') as strainer:
            with mock.patch('flavors.BeautifulSoup') as bs:
                strainer.return_value = 'SoupStrainer Object'
                spans = mock.Mock()
                spans.return_value = mock_flavors
                bs.return_value = spans
                

                flavor_info = flavors.extract_flavors(mock_html)
                self.assertEqual(flavor_info,expected_flavors)
                strainer.assert_called_with('span', ['flavorhead','flavorheadwhite', 'flavorcap', 'flavorcapwhite'])
                bs.assert_called_with(mock_html,'html.parser',parse_only='SoupStrainer Object')
                spans.assert_called_with('span')    







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









