# Python
import csv, cStringIO

# Django
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

# Third Party
from tastypie.serializers import Serializer
from tastypie.models import ApiKey

# Project
from data.models import (HeadTeacher, SchoolData, TeacherPerformanceData,
                         SchoolMonitoringData,
                         LearnerPerformanceData, InboundSMS, AcademicAchievementCode)
from data.tests import utils

class TestDataCSVAPI(TestCase):
    fixtures = ['data.json', 'hierarchy.json', 'academic_achievement_code.json']

    def setUp(self):
      self.user = User.objects.create(username="username")
      self.api_key = ApiKey.objects.create(user=self.user)
      self.api_key.key = self.api_key.generate_key()
      self.api_key.save()

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
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
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

    def test_head_teacher_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/headteacher',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')

    def test_school_data_csv_api(self):
        utils.create_school_data()
        utils.create_school_data()
        utils.create_school_data()
        utils.create_school_data()

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/school',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
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
                              unicode(obj.boys),
                              unicode(obj.girls),
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
                                      "girls",
                                      "boys",
                                      "created_at",
                                      "created_by",
                                      "emis"]))
        self.assertEqual(sorted(response_list), sorted(object_list))

    def test_school_data_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/school',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')


    def test_school_monitoring_csv_api(self):
        """
            Testing basic school monitoring API functionality.
        """
        utils.create_school_monitoring_data()
        utils.create_school_monitoring_data()

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/school_monitoring',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)

        response_list = self.parse_csv_response(response.content)
        db_objects = SchoolMonitoringData.objects.all()

        object_list = [sorted([unicode(obj.see_lpip),
                              unicode(obj.teaching),
                              unicode(obj.learner_assessment),
                              unicode(obj.learning_materials),
                              unicode(obj.learner_attendance),
                              unicode(obj.reading_time),
                              unicode(obj.struggling_learners),
                              unicode(obj.g2_observation_results),
                              unicode(obj.ht_feedback),
                              unicode(obj.submitted_classroom),
                              unicode(obj.gala_sheets),
                              unicode(obj.ht_feedback_literacy),
                              unicode(obj.summary_worksheet),
                              unicode(obj.submitted_gala),
                              unicode(obj.talking_wall),
                              self.convert_date_time_to_tastypie(obj.created_at),
                              unicode(obj.created_by.id),
                              unicode(obj.emis.id),
                              unicode(obj.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["see_lpip",
                                      "teaching",
                                      "learner_assessment",
                                      "learning_materials",
                                      "learner_attendance",
                                      "reading_time",
                                      "struggling_learners",
                                      "g2_observation_results",
                                      "ht_feedback",
                                      "submitted_classroom",
                                      "gala_sheets",
                                      "ht_feedback_literacy",
                                      "summary_worksheet",
                                      "submitted_gala",
                                      "talking_wall",
                                      "created_at",
                                      "created_by",
                                      "emis",
                                      "id"]))
        self.assertEqual(sorted(response_list), sorted(object_list))

    def test_school_monitoring_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/school_monitoring',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')

    def test_teacher_perfomance_csv_api(self):
        """
            Testing basic teacher performance API functionality.
        """
        utils.create_teacher_perfomance_data()
        utils.create_teacher_perfomance_data()

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/teacherperformance',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)

        response_list = self.parse_csv_response(response.content)
        db_objects = TeacherPerformanceData.objects.all()

        object_list = [sorted([unicode(obj.gender),
                              unicode(obj.age),
                              unicode(obj.years_experience),
                              unicode(obj.g2_pupils_present),
                              unicode(obj.g2_pupils_registered),
                              unicode(obj.classroom_environment_score),
                              unicode(obj.t_l_materials),
                              unicode(obj.created_by.id),
                              unicode(obj.pupils_materials_score),
                              unicode(obj.pupils_books_number),
                              unicode(obj.reading_lesson),
                              unicode(obj.pupil_engagement_score),
                              unicode(obj.attitudes_and_beliefs),
                              unicode(obj.training_subtotal),
                              unicode(obj.ts_number),
                              unicode(obj.reading_assessment),
                              unicode(obj.reading_total),
                              unicode(obj.academic_level.id),
                              self.convert_date_time_to_tastypie(obj.created_at),
                              unicode(obj.emis.id),
                              unicode(obj.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["gender",
                                      "age",
                                      "years_experience",
                                      "g2_pupils_present",
                                      "g2_pupils_registered",
                                      "classroom_environment_score",
                                      "t_l_materials",
                                      "pupils_materials_score",
                                      "pupils_books_number",
                                      "reading_lesson",
                                      "pupil_engagement_score",
                                      "attitudes_and_beliefs",
                                      "training_subtotal",
                                      "ts_number",
                                      "reading_assessment",
                                      "reading_total",
                                      "academic_level",
                                      "created_at",
                                      "created_by",
                                      "emis",
                                      "id"]))
        self.assertEqual(sorted(response_list), sorted(object_list))

    def test_teacher_perfomance_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/teacherperformance',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')

    def test_learner_perfomance_csv_api(self):
        """
            Testing basic learner performance API functionality.
        """
        utils.create_learner_perfomance_data()
        utils.create_learner_perfomance_data()

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/learnerperformance',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)

        response_list = self.parse_csv_response(response.content)
        db_objects = LearnerPerformanceData.objects.all()

        object_list = [sorted([unicode(obj.gender),
                              unicode(obj.total_number_pupils),
                              unicode(obj.phonetic_awareness),
                              unicode(obj.vocabulary),
                              unicode(obj.reading_comprehension),
                              unicode(obj.writing_diction),
                              unicode(obj.below_minimum_results),
                              unicode(obj.minimum_results),
                              unicode(obj.desirable_results),
                              unicode(obj.outstanding_results),
                              unicode(obj.created_by.id),
                              self.convert_date_time_to_tastypie(obj.created_at),
                              unicode(obj.id),
                              unicode(obj.emis.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id",
                                      "gender",
                                      "total_number_pupils",
                                      "phonetic_awareness",
                                      "vocabulary",
                                      "reading_comprehension",
                                      "writing_diction",
                                      "below_minimum_results",
                                      "minimum_results",
                                      "desirable_results",
                                      "outstanding_results",
                                      "created_at",
                                      "created_by",
                                      "emis"]))
        self.assertEqual(sorted(response_list), sorted(object_list))

    def test_learner_perfomance_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/learnerperformance',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')


    def test_sms_csv_api(self):
        """
            Testing basic schooldata API functionality.
        """
        utils.create_inbound_sms()

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/sms',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)


        response_list = self.parse_csv_response(response.content)
        db_objects = InboundSMS.objects.all()

        object_list = [sorted([unicode(obj.message),
                              unicode(obj.created_by.id),
                              self.convert_date_time_to_tastypie(obj.created_at),
                              unicode(obj.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id",
                                      "message",
                                      "created_at",
                                      "created_by"]))
        self.assertEqual(sorted(response_list), sorted(object_list))

    def test_sms_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/sms',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')


    def test_academic_achievemnt_csv_api(self):
        """
            Testing basic schooldata API functionality.
        """
        utils.create_academic_level()

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/achievement',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)


        response_list = self.parse_csv_response(response.content)
        db_objects = AcademicAchievementCode.objects.all()

        object_list = [sorted([unicode(obj.achievement),
                              unicode(obj.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id",
                                      "achievement"]))
        self.assertEqual(sorted(response_list), sorted(object_list))

    def test_achievement_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/data/achievement',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')

