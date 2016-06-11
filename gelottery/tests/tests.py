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