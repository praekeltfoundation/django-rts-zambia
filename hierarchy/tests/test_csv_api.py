# -*- coding: utf-8 -*-
# Python
import csv, cStringIO

# Django
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Project
from hierarchy.models import (Province, District, Zone, School)

# Third party
from tastypie.models import ApiKey


class TestHierarchyCSVAPI(TestCase):
    fixtures = ['hierarchy.json']

    def setUp(self):
      self.user = User.objects.create(username="username")
      self.api_key = ApiKey.objects.create(user=self.user)
      self.api_key.key = self.api_key.generate_key()
      self.api_key.save()

    def parse_csv_response(self, response_content):
        csvio = cStringIO.StringIO(response_content)
        csv_response_obj = csv.reader(csvio)
        return [sorted(item) for item in csv_response_obj if item != []]

    def test_school_csv_api(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/school',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))

        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        response_list = self.parse_csv_response(response.content)
        db_objects = School.objects.all()
        object_list = [sorted(["/api/v1/zone/" + str(obj.display_zone().id) + "/",
                              unicode(obj.display_zone().name),
                              str(obj.display_district().id),
                              unicode(obj.display_district().name),
                              str(obj.display_province().id),
                              unicode(obj.display_province().name),
                              unicode(obj.name),
                              str(obj.emis),
                              str(obj.id),
                              str(obj.zone.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["zone_id", "zone", "district_id",
                                      "name", "district_name", "zone_name",
                                      "emis", "province_id", "id", "province_name"]))
        self.assertEqual(sorted(response_list), sorted(object_list))

    def test_school_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/school',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')


    def test_zone_csv_api(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/zone',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        response_list = self.parse_csv_response(response.content)
        db_objects = Zone.objects.all()
        object_list = [sorted([unicode(obj.name),
                              str(obj.id),
                              str(obj.district.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id", "district", "name"]))
        self.assertEqual(sorted(response_list), sorted(object_list))

    def test_zone_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/zone',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')


    def test_district_csv_api(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/district',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        response_list = self.parse_csv_response(response.content)
        db_objects = District.objects.all()
        object_list = [sorted([unicode(obj.name),
                              str(obj.id),
                              str(obj.province.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id", "province", "name"]))
        self.assertEqual(sorted(response_list), sorted(object_list))

    def test_district_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/district',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')


    def test_province_csv_api(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/province',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        response_list = self.parse_csv_response(response.content)
        db_objects = Province.objects.all()
        object_list = [sorted([unicode(obj.name),
                              str(obj.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id", "name"]))
        self.assertEqual(sorted(response_list), sorted(object_list))

    def test_province_csv_api_unauthorized(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/province',
                      'api_name': 'v1'})
        response = self.client.get(url)

        self.assertEqual("text/plain; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, 'Sorry you are not authorized!')

    def test_non_unicode_csv_api(self):
        # This tests that the response from the API corresponds with the model
        # Creating a non unicode character
        Province.objects.get_or_create(name=u"Zoè")

        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/province',
                      'api_name': 'v1'})
        response = self.client.get("%s?api_key=%s&username=%s" % (url, self.api_key.key, self.user.username))
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)

        response_list = self.parse_csv_response(response.content)
        db_objects = Province.objects.all()

        # Using same encoding that is used in Tasypie
        object_list = [sorted([obj.name.encode("utf-8"),
                              str(obj.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id", "name"]))
        self.assertEqual(sorted(response_list), sorted(object_list))
