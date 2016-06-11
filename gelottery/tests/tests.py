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