# Python
import datetime
import json

# Django
from django.core.urlresolvers import reverse

# Thirdy Party
from tastypie.test import ResourceTestCase

# Project
from data.models import (HeadTeacher, SchoolData, TeacherPerformanceData,
                         LearnerPerformanceData, InboundSMS, DistrictAdminUser)
from data.tests import utils



class TestDistrictAdmin(ResourceTestCase):
    fixtures = ['data.json', 'hierarchy.json', 'academic_achievement_code.json']

    def setUp(self):
        # Need to do super() for the tastypie setUp funcs
        super(TestDistrictAdmin, self).setUp()
        self.dist_admin_url = reverse('api_dispatch_list',
                                      kwargs={'resource_name': 'district_admin',
                                      'api_name': 'v1'})

    def test_basic_api_functionality(self):
        # Checks if there is actually and endpoint
        response = self.api_client.get(self.dist_admin_url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)


    def test_post_good_disrict_admin_data(self):
        # Checks if data can be posted to the API
        district = utils.create_district()
        data = {"first_name": "test_first_name",
                "last_name": "test_last_name",
                "date_of_birth": "2012-10-12T10:00:00",
                "district": "/api/v1/district/%s/" % district.id,
                "id_number": "za123456789",
                }

        response = self.api_client.post(self.dist_admin_url, format="json", data=data)

        # Testing the JSON response
        json_item = json.loads(response.content)
        self.assertEqual(data["first_name"], json_item["first_name"])
        self.assertEqual(data["last_name"], json_item["last_name"])
        self.assertEqual(data["date_of_birth"], json_item["date_of_birth"])
        self.assertEqual(data["id_number"], json_item["id_number"])
        self.assertEqual(district.name, json_item["district"]["name"])

        district_admin = DistrictAdminUser.objects.get(id=json_item["id"])
        self.assertEqual(data["first_name"], district_admin.first_name)
        self.assertEqual(data["last_name"], district_admin.last_name)
        self.assertEqual(datetime.date(2012, 10, 12), district_admin.date_of_birth)
        self.assertEqual(data["id_number"], district_admin.id_number)
        self.assertEqual(district.name, district_admin.district.name)

    def test_post_with_non_existent_district_for_district_admin_data(self):
        data = {"first_name": "test_first_name",
                "last_name": "test_last_name",
                "date_of_birth": "2012-10-12T10:00:00",
                "district": "/api/v1/district/%s/" % 1212, # Non existent district
                "id_number": "za123456789",
                }
        response = self.api_client.post(self.dist_admin_url, format="json", data=data)
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)


    def test_good_post_teacherperformance_json_data_by_district_admin(self):
        district_admin = utils.create_district_admin()

        response = self.api_client.get("%s%s/" % (self.dist_admin_url, district_admin.id))
        json_item = json.loads(response.content)

        district_admin_uri = json_item['resource_uri']
        district_admin_id = json_item['id']

        url = reverse('api_dispatch_detail',
                      kwargs={'resource_name': 'data/achievement',
                      'api_name': 'v1', "pk": 8})
        response = self.api_client.get((url))
        json_item = json.loads(response.content)
        achievement_uri = json_item['resource_uri']
        self.assertEqual(url, achievement_uri)

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/teacherperformance',
                      'api_name': 'v1'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"gender": "male",
                                    "age": 30,
                                    "years_experience": "11+",
                                    "g2_pupils_present": 40,
                                    "g2_pupils_registered": 50,
                                    "classroom_environment_score": 15,
                                    "t_l_materials": 12,
                                    "pupils_materials_score": 13,
                                    "pupils_books_number": 14,
                                    "reading_lesson": 15,
                                    "pupil_engagement_score": 16,
                                    "attitudes_and_beliefs": 17,
                                    "training_subtotal": 18,
                                    "ts_number": 19,
                                    "reading_assessment": 50,
                                    "reading_total": 70,
                                    "academic_level": achievement_uri,
                                    "created_by_da": district_admin_uri,
                                    "emis": "/api/v1/school/emis/4813/"
                                    })

        json_item = json.loads(response.content)

        self.assertEqual("male", json_item["gender"])
        self.assertEqual(30, json_item["age"])
        self.assertEqual("11+", json_item["years_experience"])
        self.assertEqual(40, json_item["g2_pupils_present"])
        self.assertEqual(50, json_item["g2_pupils_registered"])
        self.assertEqual(15, json_item["classroom_environment_score"])
        self.assertEqual(12, json_item["t_l_materials"])
        self.assertEqual(13, json_item["pupils_materials_score"])
        self.assertEqual(14, json_item["pupils_books_number"])
        self.assertEqual(15, json_item["reading_lesson"])
        self.assertEqual(16, json_item["pupil_engagement_score"])
        self.assertEqual(17, json_item["attitudes_and_beliefs"])
        self.assertEqual(18, json_item["training_subtotal"])
        self.assertEqual(19, json_item["ts_number"])
        self.assertEqual(50, json_item["reading_assessment"])
        self.assertEqual(70, json_item["reading_total"])
        self.assertEqual(8, json_item["academic_level"]["id"])
        self.assertEqual(4813, json_item["emis"]["emis"])
        self.assertEqual("Musungu", json_item["emis"]["name"])
        self.assertFalse(json_item["created_by"])
        self.assertEqual(district_admin_uri, json_item["created_by_da"]["resource_uri"])
        self.assertEqual(district_admin_id, json_item["created_by_da"]["id"])

        teacher = TeacherPerformanceData.objects.get(pk=json_item["id"])
        self.assertEqual("male", teacher.gender)
        self.assertEqual(30, teacher.age)
        self.assertEqual("11+", teacher.years_experience)
        self.assertEqual(40, teacher.g2_pupils_present)
        self.assertEqual(50, teacher.g2_pupils_registered)
        self.assertEqual(15, teacher.classroom_environment_score)
        self.assertEqual(12, teacher.t_l_materials)
        self.assertEqual(13, teacher.pupils_materials_score)
        self.assertEqual(14, teacher.pupils_books_number)
        self.assertEqual(15, teacher.reading_lesson)
        self.assertEqual(16, teacher.pupil_engagement_score)
        self.assertEqual(17, teacher.attitudes_and_beliefs)
        self.assertEqual(18, teacher.training_subtotal)
        self.assertEqual(19, teacher.ts_number)
        self.assertEqual(50, teacher.reading_assessment)
        self.assertEqual(70, teacher.reading_total)
        self.assertEqual(8, teacher.academic_level.id)
        self.assertIsNotNone(teacher.created_at)
        self.assertEqual("Musungu", teacher.emis.name)
        self.assertEqual(district_admin_id, teacher.created_by_da.id)
        self.assertFalse(teacher.created_by)


    def test_good_post_learnerperformance_json_data_by_district_admin(self):
        district_admin = utils.create_district_admin()

        response = self.api_client.get("%s%s/" % (self.dist_admin_url, district_admin.id))
        json_item = json.loads(response.content)

        district_admin_uri = json_item['resource_uri']
        district_admin_id = json_item['id']

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/learnerperformance',
                      'api_name': 'v1'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"gender": "female",
                                    "total_number_pupils": 40,
                                    "phonetic_awareness": 50,
                                    "vocabulary": 15,
                                    "reading_comprehension": 12,
                                    "writing_diction": 13,
                                    "below_minimum_results": 14,
                                    "minimum_results": 15,
                                    "desirable_results": 16,
                                    "outstanding_results": 17,
                                    "created_by_da": district_admin_uri,
                                    "emis": "/api/v1/school/emis/4813/"
                                    })

        json_item = json.loads(response.content)
        self.assertEqual("female", json_item["gender"])
        self.assertEqual(40, json_item["total_number_pupils"])
        self.assertEqual(50, json_item["phonetic_awareness"])
        self.assertEqual(15, json_item["vocabulary"])
        self.assertEqual(12, json_item["reading_comprehension"])
        self.assertEqual(13, json_item["writing_diction"])
        self.assertEqual(14, json_item["below_minimum_results"])
        self.assertEqual(15, json_item["minimum_results"])
        self.assertEqual(16, json_item["desirable_results"])
        self.assertEqual(17, json_item["outstanding_results"])
        self.assertEqual(4813, json_item["emis"]["emis"])
        self.assertEqual("Musungu", json_item["emis"]["name"])
        self.assertFalse(json_item["created_by"])
        self.assertEqual(district_admin_uri, json_item["created_by_da"]["resource_uri"])
        self.assertEqual(district_admin_id, json_item["created_by_da"]["id"])

        learner = LearnerPerformanceData.objects.all()[0]
        self.assertEqual("female", learner.gender)
        self.assertEqual(40, learner.total_number_pupils)
        self.assertEqual(50, learner.phonetic_awareness)
        self.assertEqual(15, learner.vocabulary)
        self.assertEqual(12, learner.reading_comprehension)
        self.assertEqual(13, learner.writing_diction)
        self.assertEqual(14, learner.below_minimum_results)
        self.assertEqual(15, learner.minimum_results)
        self.assertEqual(16, learner.desirable_results)
        self.assertEqual(17, learner.outstanding_results)
        self.assertIsNotNone(learner.created_at)
        self.assertEqual("Musungu", learner.emis.name)
        self.assertEqual(4813, learner.emis.emis)
        self.assertEqual(district_admin_id, learner.created_by_da.id)
        self.assertFalse(learner.created_by)



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
                      'api_name': 'v1'})
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
                      'api_name': 'v1'})
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
                      'api_name': 'v1'})
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


class TestHeadTeacherData(ResourceTestCase):
    fixtures = ['data.json', 'hierarchy.json']

    def test_is_zonal_head_true(self):
        """
            Testing basic API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/headteacher',
                      'api_name': 'v1'})
        response = self.client.get("%s?is_zonal_head=True" % url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)
        [self.assertEqual(dict_item["is_zonal_head"], True) for dict_item in json_item["objects"]]
        self.assertEqual(len(json_item["objects"]), 1)

    def test_is_zonal_head_false(self):
        """
            Testing basic API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/headteacher',
                      'api_name': 'v1'})
        response = self.client.get("%s?is_zonal_head=False" % url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)
        [self.assertEqual(dict_item["is_zonal_head"], False) for dict_item in json_item["objects"]]
        self.assertEqual(len(json_item["objects"]), 3)


class TestSchoolDataAPI(ResourceTestCase):
    fixtures = ['data.json', 'hierarchy.json']

    def test_basic_api_functionality(self):
        """
            Testing basic schooldata API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/school',
                      'api_name': 'v1'})
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
                      'api_name': 'v1'})
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
                      'api_name': 'v1'})
        response = self.api_client.get("%s?emis__emis=4813" % (url))
        json_item = json.loads(response.content)
        headteacher_uri = json_item['objects'][0]['resource_uri']
        headteacher_id = json_item['objects'][0]['id']

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/school',
                      'api_name': 'v1'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"name": "test_name",
                                    "classrooms": 30,
                                    "teachers": 40,
                                    "boys": 115,
                                    "girls": 120,
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
        self.assertEqual(115, json_item["boys"])
        self.assertEqual(120, json_item["girls"])
        self.assertEqual("Musungu", json_item["emis"]["name"])

        schooldata = SchoolData.objects.get(pk=1)
        self.assertEqual("test_name", schooldata.name)
        self.assertEqual(30, schooldata.classrooms)
        self.assertEqual(40, schooldata.teachers)
        self.assertEqual(4, schooldata.teachers_g1)
        self.assertEqual(8, schooldata.teachers_g2)
        self.assertEqual(15, schooldata.boys_g2)
        self.assertEqual(115, schooldata.boys)
        self.assertEqual(120, schooldata.girls)
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
                      kwargs={'resource_name': 'data/school',
                      'api_name': 'v1'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"name": "test_name",
                                    "classrooms": 30,
                                    "teachers": 40,
                                    "teachers_g1": 4,
                                    "teachers_g2": 8,
                                    "boys_g2": 15,
                                    "girls_g2": 12,
                                    "created_by": "/api/v1/data/school/9999/",
                                    "emis": "/api/v1/school/emis/4813/"
                                    })
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)


class TestTeacherPerformanceDataAPI(ResourceTestCase):
    fixtures = ['data.json', 'hierarchy.json', 'academic_achievement_code.json']

    def test_basic_api_functionality(self):
        """
            Testing basic teacher performance API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/teacherperformance',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)

    def test_good_post_teacherperformance_json_data(self):
        """
            Testing good post teacher performance data.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/headteacher',
                      'api_name': 'v1'})
        response = self.api_client.get("%s?emis__emis=4813" % (url))
        json_item = json.loads(response.content)
        headteacher_uri = json_item['objects'][0]['resource_uri']
        headteacher_id = json_item['objects'][0]['id']

        url = reverse('api_dispatch_detail',
                      kwargs={'resource_name': 'data/achievement',
                      'api_name': 'v1', "pk": 8})
        response = self.api_client.get((url))
        json_item = json.loads(response.content)
        achievement_uri = json_item['resource_uri']
        self.assertEqual(url, achievement_uri)

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/teacherperformance',
                      'api_name': 'v1'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"gender": "male",
                                    "age": 30,
                                    "years_experience": "11+",
                                    "g2_pupils_present": 40,
                                    "g2_pupils_registered": 50,
                                    "classroom_environment_score": 15,
                                    "t_l_materials": 12,
                                    "pupils_materials_score": 13,
                                    "pupils_books_number": 14,
                                    "reading_lesson": 15,
                                    "pupil_engagement_score": 16,
                                    "attitudes_and_beliefs": 17,
                                    "training_subtotal": 18,
                                    "ts_number": 19,
                                    "reading_assessment": 50,
                                    "reading_total": 70,
                                    "academic_level": achievement_uri,
                                    "created_by": headteacher_uri,
                                    "emis": "/api/v1/school/emis/4813/"
                                    })

        json_item = json.loads(response.content)
        self.assertEqual("male", json_item["gender"])
        self.assertEqual(30, json_item["age"])
        self.assertEqual("11+", json_item["years_experience"])
        self.assertEqual(40, json_item["g2_pupils_present"])
        self.assertEqual(50, json_item["g2_pupils_registered"])
        self.assertEqual(15, json_item["classroom_environment_score"])
        self.assertEqual(12, json_item["t_l_materials"])
        self.assertEqual(13, json_item["pupils_materials_score"])
        self.assertEqual(14, json_item["pupils_books_number"])
        self.assertEqual(15, json_item["reading_lesson"])
        self.assertEqual(16, json_item["pupil_engagement_score"])
        self.assertEqual(17, json_item["attitudes_and_beliefs"])
        self.assertEqual(18, json_item["training_subtotal"])
        self.assertEqual(19, json_item["ts_number"])
        self.assertEqual(50, json_item["reading_assessment"])
        self.assertEqual(70, json_item["reading_total"])
        self.assertEqual(8, json_item["academic_level"]["id"])
        self.assertEqual(4813, json_item["emis"]["emis"])
        self.assertEqual("Musungu", json_item["emis"]["name"])
        self.assertFalse(json_item["created_by_da"])
        self.assertEqual(headteacher_uri, json_item["created_by"]["resource_uri"])
        self.assertEqual(headteacher_id, json_item["created_by"]["id"])

        teacher = TeacherPerformanceData.objects.get(pk=1)
        self.assertEqual("male", teacher.gender)
        self.assertEqual(30, teacher.age)
        self.assertEqual("11+", teacher.years_experience)
        self.assertEqual(40, teacher.g2_pupils_present)
        self.assertEqual(50, teacher.g2_pupils_registered)
        self.assertEqual(15, teacher.classroom_environment_score)
        self.assertEqual(12, teacher.t_l_materials)
        self.assertEqual(13, teacher.pupils_materials_score)
        self.assertEqual(14, teacher.pupils_books_number)
        self.assertEqual(15, teacher.reading_lesson)
        self.assertEqual(16, teacher.pupil_engagement_score)
        self.assertEqual(17, teacher.attitudes_and_beliefs)
        self.assertEqual(18, teacher.training_subtotal)
        self.assertEqual(19, teacher.ts_number)
        self.assertEqual(50, teacher.reading_assessment)
        self.assertEqual(70, teacher.reading_total)
        self.assertEqual(8, teacher.academic_level.id)
        self.assertIsNotNone(teacher.created_at)
        self.assertEqual("Musungu", teacher.emis.name)
        self.assertEqual(4813, teacher.emis.emis)
        self.assertEqual(4813, teacher.created_by.emis.emis)
        self.assertEqual(headteacher_id, teacher.created_by.id)
        self.assertFalse(teacher.created_by_da)


class TestLearnerPerformanceDataAPI(ResourceTestCase):
    fixtures = ['data.json', 'hierarchy.json']

    def test_basic_api_functionality(self):
        """
            Testing basic learner performance API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/learnerperformance',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)

    def test_good_post_learnerperformance_json_data(self):
        """
            Testing good post learner performance data.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/headteacher',
                      'api_name': 'v1'})
        response = self.api_client.get("%s?emis__emis=4813" % (url))
        json_item = json.loads(response.content)
        headteacher_uri = json_item['objects'][0]['resource_uri']
        headteacher_id = json_item['objects'][0]['id']

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/learnerperformance',
                      'api_name': 'v1'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"gender": "female",
                                    "total_number_pupils": 40,
                                    "phonetic_awareness": 50,
                                    "vocabulary": 15,
                                    "reading_comprehension": 12,
                                    "writing_diction": 13,
                                    "below_minimum_results": 14,
                                    "minimum_results": 15,
                                    "desirable_results": 16,
                                    "outstanding_results": 17,
                                    "created_by": headteacher_uri,
                                    "emis": "/api/v1/school/emis/4813/"
                                    })

        json_item = json.loads(response.content)
        self.assertEqual("female", json_item["gender"])
        self.assertEqual(40, json_item["total_number_pupils"])
        self.assertEqual(50, json_item["phonetic_awareness"])
        self.assertEqual(15, json_item["vocabulary"])
        self.assertEqual(12, json_item["reading_comprehension"])
        self.assertEqual(13, json_item["writing_diction"])
        self.assertEqual(14, json_item["below_minimum_results"])
        self.assertEqual(15, json_item["minimum_results"])
        self.assertEqual(16, json_item["desirable_results"])
        self.assertEqual(17, json_item["outstanding_results"])
        self.assertEqual(4813, json_item["emis"]["emis"])
        self.assertEqual("Musungu", json_item["emis"]["name"])

        learner = LearnerPerformanceData.objects.all()[0]
        self.assertEqual("female", learner.gender)
        self.assertEqual(40, learner.total_number_pupils)
        self.assertEqual(50, learner.phonetic_awareness)
        self.assertEqual(15, learner.vocabulary)
        self.assertEqual(12, learner.reading_comprehension)
        self.assertEqual(13, learner.writing_diction)
        self.assertEqual(14, learner.below_minimum_results)
        self.assertEqual(15, learner.minimum_results)
        self.assertEqual(16, learner.desirable_results)
        self.assertEqual(17, learner.outstanding_results)
        self.assertIsNotNone(learner.created_at)
        self.assertEqual("Musungu", learner.emis.name)
        self.assertEqual(4813, learner.emis.emis)
        self.assertEqual(4813, learner.created_by.emis.emis)
        self.assertEqual(headteacher_id, learner.created_by.id)


class TestInboudSMSAPI(ResourceTestCase):
    fixtures = ['data.json', 'hierarchy.json']

    def test_basic_api_functionality(self):
        """
            Testing basic schooldata API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/sms',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        json_item = json.loads(response.content)
        self.assertIn("meta", json_item)
        self.assertIn("objects", json_item)


    def test_good_post_sms_data(self):
        """
            Testing good post sms data.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/headteacher',
                      'api_name': 'v1'})
        response = self.api_client.get("%s?emis__emis=4813" % (url))
        json_item = json.loads(response.content)
        headteacher_uri = json_item['objects'][0]['resource_uri']
        headteacher_id = json_item['objects'][0]['id']

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/sms',
                      'api_name': 'v1'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"message": "This is the sms",
                                    "created_by": headteacher_uri,
                                    })

        json_item = json.loads(response.content)
        self.assertEqual("This is the sms", json_item["message"])
        self.assertEqual("/api/v1/data/sms/1/", json_item["resource_uri"])
        self.assertEqual(4813, json_item["created_by"]["emis"]["emis"])
        self.assertEqual("Musungu", json_item["created_by"]["emis"]["name"])

        sms = InboundSMS.objects.get(pk=1)
        self.assertEqual("This is the sms", sms.message)
        self.assertIsNotNone(sms.created_at)
        self.assertEqual("Musungu", sms.created_by.emis.name)
        self.assertEqual(4813, sms.created_by.emis.emis)
        self.assertEqual(headteacher_id, sms.created_by.id)

    def test_bad_uri_post_headteacher_data(self):
        """
            Testing bad post sms data.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'data/sms',
                      'api_name': 'v1'})
        response = self.api_client.post(url,
                                    format="json",
                                    data={"message": "This is the sms",
                                    "created_by": "/api/v1/data/headteacher/121212/",
                                    })
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)
