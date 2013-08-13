from django.test import TestCase
from tastypie.test import ResourceTestCase
from django.core.urlresolvers import reverse
import json
from data.models import HeadTeacher, SchoolData
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

    def test_good_post_headteacher_data(self):
        """
            Testing headteacher post data.
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
                                    "emis": "/api/v1/school/emis/4813/"
                                    })

        json_item = json.loads(response.content)
        self.assertEqual("test_first_name", json_item["first_name"])
        self.assertEqual("test_last_name", json_item["last_name"])

        self.assertEqual("2012-10-12T10:00:00", json_item["date_of_birth"])
        self.assertEqual("male", json_item["gender"])
        self.assertEqual("0123456789", json_item["msisdn"])
        self.assertEqual(4813, json_item["emis"]["emis"])
        self.assertEqual("Musungu", json_item["emis"]["name"])

        headteacher = HeadTeacher.objects.all()[0]
        self.assertEqual("test_first_name", headteacher.first_name)
        self.assertEqual("test_last_name", headteacher.last_name)
        self.assertEqual(2, headteacher.emis_id)
        self.assertEqual("male", headteacher.gender)
        self.assertEqual(False, headteacher.is_zonal_head)
        self.assertEqual( datetime.date(2012, 10, 12), headteacher.date_of_birth)
        self.assertIsNotNone(headteacher.created_at)
        self.assertEqual("Musungu", headteacher.emis.name)
        self.assertEqual(4813, headteacher.emis.emis)

    def test_bad_emis_post_headteacher_data(self):
        """
            Testing headteacher post data.
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
                                    "emis": "/api/v1/school/emis/121281/"
                                    })
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)

    def test_empty_emis_post_headteacher_data(self):
        """
            Testing headteacher post data.
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
                                    })
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)



class TestSchoolDataAPI(ResourceTestCase):
    fixtures = ['data.json', 'hierarchy.json']

    def test_basic_api_functionality(self):
        """
            Testing basic schooldata API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/schooldata',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)

    def test_headteacher_get_filter_emis(self):
        """
        Testing the filtering functionality on emis
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/headteacher',
                      'api_name': 'api'})
        response = self.api_client.get("%s?emis__emis=4813" % (url))
        json_item = json.loads(response.content)
        self.assertEqual(1, json_item["meta"]["total_count"])
        self.assertEqual("xyz", json_item["objects"][0]["first_name"])
        self.assertEqual("zyx", json_item["objects"][0]["last_name"])

        self.assertEqual("1952-10-12", json_item["objects"][0]["date_of_birth"])
        self.assertEqual("male", json_item["objects"][0]["gender"])
        self.assertEqual("072111111", json_item["objects"][0]["msisdn"])
        self.assertEqual(4813, json_item["objects"][0]["emis"]["emis"])
        self.assertEqual("Musungu", json_item["objects"][0]["emis"]["name"])

        self.assertEqual("/api/v1/school/2/", json_item["objects"][0]["emis"]["resource_uri"])
        self.assertEqual("Mesenge", json_item["objects"][0]["emis"]["zone"]["name"])

    def test_good_post_schooldata_json_data(self):
        """
            Testing good post school data.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/headteacher',
                      'api_name': 'api'})
        response = self.api_client.get("%s?emis__emis=4813" % (url))
        json_item = json.loads(response.content)
        headteacher_uri = json_item['objects'][0]['resource_uri']
        headteacher_id = json_item['objects'][0]['id']

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/schooldata',
                      'api_name': 'api'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"name": "test_name",
                                    "classrooms": 30,
                                    "teachers": 40,
                                    "teachers_g1": 4,
                                    "teachers_g2": 8,
                                    "boys_g2": 15,
                                    "girls_g2": 12,
                                    "created_by": headteacher_uri,
                                    "emis": "/api/v1/school/emis/4813/"
                                    })

        json_item = json.loads(response.content)
        self.assertEqual("test_name", json_item["name"])
        self.assertEqual(30, json_item["classrooms"])

        self.assertEqual(40, json_item["teachers"])
        self.assertEqual(4, json_item["teachers_g1"])
        self.assertEqual(8, json_item["teachers_g2"])
        self.assertEqual(15, json_item["boys_g2"])
        self.assertEqual(12, json_item["girls_g2"])
        self.assertEqual(4813, json_item["emis"]["emis"])
        self.assertEqual("Musungu", json_item["emis"]["name"])

        schooldata = SchoolData.objects.get(pk=1)
        self.assertEqual("test_name", schooldata.name)
        self.assertEqual(30, schooldata.classrooms)
        self.assertEqual(40, schooldata.teachers)
        self.assertEqual(4, schooldata.teachers_g1)
        self.assertEqual(8, schooldata.teachers_g2)
        self.assertEqual(15, schooldata.boys_g2)
        self.assertEqual(12, schooldata.girls_g2)
        self.assertIsNotNone(schooldata.created_at) 
        self.assertEqual("Musungu", schooldata.emis.name)
        self.assertEqual(4813, schooldata.emis.emis)
        self.assertEqual(4813, schooldata.created_by.emis.emis)
        self.assertEqual(headteacher_id, schooldata.created_by.id)

    def test_bad_uri_post_headteacher_data(self):
        """
            Testing headteacher post data.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/schooldata',
                      'api_name': 'api'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"name": "test_name",
                                    "classrooms": 30,
                                    "teachers": 40,
                                    "teachers_g1": 4,
                                    "teachers_g2": 8,
                                    "boys_g2": 15,
                                    "girls_g2": 12,
                                    "created_by": "/api/data/schooldata/9999/",
                                    "emis": "/api/v1/school/emis/4813/"
                                    })
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)


class TestTeacherPerfomanceDataAPI(ResourceTestCase):
    fixtures = ['data.json', 'hierarchy.json']

    def test_basic_api_functionality(self):
        """
            Testing basic teacher perfomance API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/teacherperfomance',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)


class TestLearnerPerfomanceDataAPI(ResourceTestCase):
    fixtures = ['data.json', 'hierarchy.json']

    def test_basic_api_functionality(self):
        """
            Testing basic learner perfomance API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/learnerperfomance',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)