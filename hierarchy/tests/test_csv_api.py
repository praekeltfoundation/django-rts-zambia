# Python
import csv, cStringIO

# Django
from django.test import TestCase
from django.core.urlresolvers import reverse

# Project
from hierarchy.models import (Province, District, Zone, School)


class TestHierarchyCSVAPI(TestCase):
    fixtures = ['hierarchy.json']

    def parse_csv_response(self, response_content):
        csvio = cStringIO.StringIO(response_content)
        csv_response_obj = csv.reader(csvio)
        return [sorted(item) for item in csv_response_obj if item != []]

    def test_school_csv_api(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/school',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        response_list = self.parse_csv_response(response.content)
        db_objects = School.objects.all()
        object_list = [sorted([unicode(obj.name),
                              str(obj.emis),
                              str(obj.id),
                              str(obj.zone.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id", "emis", "zone", "name"]))
        self.assertEqual(sorted(response_list), sorted(object_list))


    def test_zone_csv_api(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/zone',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        response_list = self.parse_csv_response(response.content)
        db_objects = Zone.objects.all()
        object_list = [sorted([unicode(obj.name),
                              str(obj.id),
                              str(obj.district.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id", "district", "name"]))
        self.assertEqual(sorted(response_list), sorted(object_list))


    def test_district_csv_api(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/district',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        response_list = self.parse_csv_response(response.content)
        db_objects = District.objects.all()
        object_list = [sorted([unicode(obj.name),
                              str(obj.id),
                              str(obj.province.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id", "province", "name"]))
        self.assertEqual(sorted(response_list), sorted(object_list))


    def test_province_csv_api(self):
        # This tests that the response from the API corresponds with the model
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'csv/province',
                      'api_name': 'v1'})
        response = self.client.get(url)
        self.assertEqual("text/csv; charset=utf-8", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        response_list = self.parse_csv_response(response.content)
        db_objects = Province.objects.all()
        object_list = [sorted([unicode(obj.name),
                              str(obj.id)]) for obj in db_objects]

        object_list.insert(0, sorted(["id", "name"]))
        self.assertEqual(sorted(response_list), sorted(object_list))
