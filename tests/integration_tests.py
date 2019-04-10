from bonsai_api import app
from unittest import TestCase
import json
import sys

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    # We check that a GET request on /activities/ with a "lim" parameter of 5 returns a JSON with 5 entries only.
    def test_activities_list_with_limit(self):
        response = self.app.get('/activities/', query_string='lim=5')
        self.assertEqual(
            len(list(json.loads(response.get_data().decode(sys.getdefaultencoding())))),5)
        
    # We check that a GET request on /activities/ without a limit defined will return a JSON of length 100.
    def test_activities_list(self):
        response = self.app.get('/activities/')
        self.assertEqual(
            len(list(json.loads(response.get_data().decode(sys.getdefaultencoding())))),100)
        
    # We check that a GET request on /activities/ with an invalid "lim" parameter returns a useful error message.
    def test_activities_list_invalid_lim(self):
        response = self.app.get('/activities/', query_string='lim=6d')
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())),{"message": "The 'lim' parameter does not seem to be of type integer."})