from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse


class TestAdminVArea(TestCase):
    fixtures = ['test_hierarchy.json', 'test_data.json']

    def setUp(self):
        self.admin = User.objects.create_superuser('admin',
                                                    'admin@test.com', 
                                                    'pass123')
        self.provinces = ['North Western', 'WESTERN', 'EASTERN', 'MUCHINGA', 'Luapula', 'Northern']
        self.districts = ['Solwezi', 'Mongu', 'CHIPATA', 'CHINSALI', 'Mansa', 'Mporokoso']
        self.zones = ['Kikombe', 'LUKWETA', 'MADZIMOYO', 'KALELA', 'Mbaso', 'Bweupe']
        self.schools = [3633, 14090, 8682, 2064, 1774, 2525]
    def test_admin_can_view_schools(self):
        self.client.login(username=self.admin.username,
                          password="pass123")

        url_index = reverse("admin:index")
        response = self.client.get(url_index)

        url = reverse("admin:hierarchy_province_changelist")
        response = self.client.get(url)
        province_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        province = []
        [province.append(k.name) for k in province_result]
        self.assertEqual(sorted(province), sorted(self.provinces))


        url = reverse("admin:hierarchy_district_changelist")
        response = self.client.get(url)
        district_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        district = []
        [district.append(k.name) for k in district_result]
        self.assertEqual(sorted(district), sorted(self.districts))


        url = reverse("admin:hierarchy_zone_changelist")
        response = self.client.get(url)
        zone_result =  response.__dict__['context_data']['cl'].__dict__['result_list']
        zone = []
        [zone.append(k.name) for k in zone_result]
        self.assertEqual(sorted(zone), sorted(self.zones))


        url = reverse("admin:hierarchy_school_changelist")
        response = self.client.get(url)
        school_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        school = []
        [school.append(k.emis) for k in school_result]
        self.assertEqual(sorted(school), sorted(self.schools))
