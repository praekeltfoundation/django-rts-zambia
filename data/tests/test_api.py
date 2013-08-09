from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class TestDataAPI(TestCase):
    fixtures = ['data.json', 'hierarchy.json']

    def test_basic_api_functionality(self):
        """
            Testing basic API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'hierarchy',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)

    def test_post_data(self):
        """
            Testing basic API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/headteacher',
                      'api_name': 'api'})
        response = self.client.post(url,
                                    format="json",
                                    data={"name_first": "head",
                                    "name_last": "teacher",
                                    "year": "2012-10-12T10:00:00Z",
                                    "date_of_birth": "2012-10-12T10:00:00Z",
                                    })
        print json.loads(response.content)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)