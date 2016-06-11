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

    def test_get_location_flavors(self):
        with mock.patch('flavors.get_flavor_html') as get_flavor_html:
            get_flavor_html.return_value = '<html>Test</html>'
            
            with mock.patch('flavors.extract_flavors') as extract_flavors:
                extract_flavors.return_value = {'name':'description'}
                location_flavors = flavors.get_location_flavors('13th Street')
                self.assertEqual(location_flavors,{'name':'description'})
                get_flavor_html.assert_called_with('13th Street')
                extract_flavors.assert_called_with('13th Street','<html>Test</html>')

