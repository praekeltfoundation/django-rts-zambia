from django.test import TestCase
from tastypie.test import ResourceTestCase
from django.core.urlresolvers import reverse
import json
from data.models import HeadTeacher
import datetime


class TestHeadteacherAPI(ResourceTestCase):
    fixtures = ['hierarchy.json']

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

    def test_post_headteacher_json_data(self):
        """
            Testing basic API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/headteacher',
                      'api_name': 'api'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"first_name": "test_first_name",
                                    "last_name": "test_last_name",
                                    "date_of_birth": "2012-10-12T10:00:00Z",
                                    "gender": "male",
                                    "msisdn": "0123456789",
                                    "emis": "/api/v1/school/EMIS/4813/"
                                    })

        json_item = json.loads(response.content)
        self.assertEqual("test_first_name", json_item["first_name"])
        self.assertEqual("test_last_name", json_item["last_name"])

        self.assertEqual("2012-10-12T10:00:00", json_item["date_of_birth"])
        self.assertEqual("male", json_item["gender"])
        self.assertEqual("0123456789", json_item["msisdn"])
        self.assertEqual(4813, json_item["emis"]["EMIS"])
        self.assertEqual("Musungu", json_item["emis"]["name"])

        headteacher = HeadTeacher.objects.get(pk=1)
        self.assertEqual("test_first_name", headteacher.first_name)
        self.assertEqual("test_last_name", headteacher.last_name)
        self.assertEqual(2, headteacher.emis_id)
        self.assertEqual("male", headteacher.gender)
        self.assertEqual(False, headteacher.is_zonal_head)
        self.assertEqual( datetime.date(2012, 10, 12), headteacher.date_of_birth)
        self.assertIsNotNone(headteacher.created_at)
        self.assertEqual("Musungu", headteacher.emis.name)
        self.assertEqual(4813, headteacher.emis.EMIS)



# class TestSchoolDataAPI(ResourceTestCase):
#     fixtures = ['hierarchy.json']

#     def test_basic_api_functionality(self):
#         """
#             Testing basic schooldata API functionality.
#         """
#         url = reverse('api_dispatch_list',
#                       kwargs={'resource_name': 'hierarchy',
#                       'api_name': 'v1'})
#         response = self.client.get(url)
#         self.assertEqual("application/json", response["Content-Type"])
#         self.assertEqual(response.status_code, 200)
#         json_item = json.loads(response.content)
#         self.assertIn("meta", json_item)
#         self.assertIn("objects", json_item)

#     def test_post_headteacher_json_data(self):
#         """
#             Testing posting school data.
#         """
#         url = reverse('api_dispatch_list',
#                       kwargs={'resource_name': 'data/headteacher',
#                       'api_name': 'api'})
#         response = self.api_client.post(url,
#                                     format="json",
#                                     data={"first_name": "test_first_name",
#                                     "last_name": "test_last_name",
#                                     "date_of_birth": "2012-10-12T10:00:00Z",
#                                     "gender": "male",
#                                     "msisdn": "0123456789",
#                                     "emis": "/api/v1/hierarchy/EMIS/4813/"
#                                     })

#         json_item = json.loads(response.content)
#         self.assertEqual("test_first_name", json_item["first_name"])
#         self.assertEqual("test_last_name", json_item["last_name"])

#         self.assertEqual("2012-10-12T10:00:00", json_item["date_of_birth"])
#         self.assertEqual("male", json_item["gender"])
#         self.assertEqual("0123456789", json_item["msisdn"])
#         self.assertEqual(4813, json_item["emis"]["EMIS"])
#         self.assertEqual("Musungu", json_item["emis"]["name"])

#         headteacher = HeadTeacher.objects.get(pk=1)
#         self.assertEqual("test_first_name", headteacher.first_name)
#         self.assertEqual("test_last_name", headteacher.last_name)
#         self.assertEqual(2, headteacher.emis_id)
#         self.assertEqual("male", headteacher.gender)
#         self.assertEqual(False, headteacher.is_zonal_head)
#         self.assertEqual( datetime.date(2012, 10, 12), headteacher.date_of_birth)
#         self.assertIsNotNone(headteacher.created_at)
#         self.assertEqual("Musungu", headteacher.emis.name)
#         self.assertEqual(4813, headteacher.emis.EMIS)