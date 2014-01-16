# Python
import csv, cStringIO

# Django
from django.core.urlresolvers import reverse
from django.test import TestCase

# Third Party
from tastypie.serializers import Serializer
from tastypie.test import ResourceTestCase

# Project
from data.models import (HeadTeacher, SchoolData, TeacherPerformanceData,
                         LearnerPerformanceData, InboundSMS)
from data.tests import utils

class TestDataCSVAPI(TestCase):
    fixtures = ['data.json', 'hierarchy.json', 'academic_achievement_code.json']

    def parse_csv_response(self, response_content):
        # This functions converts the csv stream into a list
        csvio = cStringIO.StringIO(response_content)
        csv_response_obj = csv.reader(csvio)
        return [sorted(item) for item in csv_response_obj if item != []]

    def convert_date_time_to_tastypie(self, dt):
        serializer = Serializer()
        return serializer.format_datetime(dt)


    def test_headteacher_csv_api(self):
        """
            Testing basic API functionality.
        """

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/headteacher',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)

        response_list = self.parse_csv_response(response.content)
        db_objects = HeadTeacher.objects.all()
        object_list = [sorted([unicode(obj.first_name),
                              unicode(obj.last_name),
                              unicode(obj.gender),
                              unicode(obj.msisdn),
                              unicode(obj.date_of_birth),
                              unicode(obj.zonal_head_name),
                              self.convert_date_time_to_tastypie(obj.created_at),
                              unicode(obj.id),
                              unicode(obj.is_zonal_head),
                              unicode(obj.emis.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id",
                                      "first_name",
                                      "last_name",
                                      "gender",
                                      "msisdn",
                                      "date_of_birth",
                                      "is_zonal_head",
                                      "zonal_head_name",
                                      "created_at",
                                      "emis"]))
        self.assertEqual(sorted(response_list), sorted(object_list))


    def test_school_data_csv_api(self):
        utils.create_school_data()
        utils.create_school_data()
        utils.create_school_data()
        utils.create_school_data()

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/school',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)

        response_list = self.parse_csv_response(response.content)
        db_objects = SchoolData.objects.all()

        object_list = [sorted([unicode(obj.name),
                              unicode(obj.classrooms),
                              unicode(obj.teachers),
                              unicode(obj.teachers_g1),
                              unicode(obj.teachers_g2),
                              unicode(obj.boys_g2),
                              unicode(obj.girls_g2),
                              unicode(obj.created_by.id),
                              self.convert_date_time_to_tastypie(obj.created_at),
                              unicode(obj.id),
                              unicode(obj.emis.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id",
                                      "name",
                                      "classrooms",
                                      "teachers",
                                      "teachers_g1",
                                      "teachers_g2",
                                      "girls_g2",
                                      "boys_g2",
                                      "created_at",
                                      "created_by",
                                      "emis"]))
        self.assertEqual(sorted(response_list), sorted(object_list))


    def test_teacher_perfomance_csv_api(self):
        """
            Testing basic teacher performance API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/teacherperformance',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)

    def test_learner_perfomance_csv_api(self):
        """
            Testing basic learner performance API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/learnerperformance',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)


    def test_sms_csv_api(self):
        """
            Testing basic schooldata API functionality.
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/sms',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)




class TestInboudSMSCSVAPI(ResourceTestCase):
    fixtures = ['data.json', 'hierarchy.json']


