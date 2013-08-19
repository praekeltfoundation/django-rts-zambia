from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib import admin


class TestAdminVArea(TestCase):
    fixtures = ['test_hierarchy.json']

    def setUp(self):
        self.admin = User.objects.create_superuser('admin',
                                                    'admin@test.com', 
                                                    'pass123')

    def test_admin_can_view_schools(self):
        self.client.login(username=self.admin.username,
                          password="pass123")

        url_index = reverse("admin:index")
        response = self.client.get(url_index)

        url = reverse("admin:hierarchy_province_changelist")
        response = self.client.get(url)
        print response.__dict__['context_data']['cl'].__dict__['result_list']


        url = reverse("admin:hierarchy_district_changelist")
        response = self.client.get(url)
        print response.__dict__['context_data']['cl'].__dict__['result_list']


        url = reverse("admin:hierarchy_zone_changelist")
        response = self.client.get(url)
        print response.__dict__['context_data']['cl'].__dict__['result_list']


        url = reverse("admin:hierarchy_school_changelist")
        response = self.client.get(url)
        print response.__dict__['context_data']['cl'].__dict__['result_list']
