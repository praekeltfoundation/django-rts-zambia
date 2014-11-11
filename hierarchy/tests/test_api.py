from django.test import TestCase
from django.core.urlresolvers import reverse
import json
from hierarchy.tests import utils


class TestHierarchyAPI(TestCase):
    fixtures = ['hierarchy.json']

    def setUp(self):
        # Need to do super() for the tastypie setUp funcs
        super(TestHierarchyAPI, self).setUp()
        self._post_save_helper = utils.PostSaveHelper()
        self._post_save_helper.replace()

    def tearDown(self):
        self._post_save_helper.restore()

    def test_basic_api_functionality(self):
        """
            Testing basic API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'school',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)
