from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse


class TestAdminView(TestCase):
    """
    Testing Super User
    """
    fixtures = ['test_hierarchy.json', 'test_data.json']

    def setUp(self):
        self.admin = User.objects.create_superuser('admin',
                                                    'admin@test.com',
                                                    'pass123')
        self.provinces = ['North Western', 'WESTERN', 'EASTERN', 'MUCHINGA', 'Luapula', 'Northern']
        self.districts = ['Solwezi', 'Mongu', 'CHIPATA', 'CHINSALI', 'Mansa', 'Mporokoso']
        self.zones = ['Kikombe', 'LUKWETA', 'MADZIMOYO', 'KALELA', 'Mbaso', 'Bweupe']
        self.schools = [3633, 14090, 8682, 2064, 1774, 2525]
        self.headteachers = [2064, 3633, 2525]
        self.schooldatas = [2064, 3633, 2525]
        self.teacherperformancedata = [2064, 3633, 2525]
        self.learnerperformancedata = [2064, 2064, 3633,  3633, 2525, 2525]
        self.inboundsms = [2064, 3633, 2525]

    def tearDown(self):
        del self.admin
        del self.provinces
        del self.districts
        del self.zones
        del self.schools
        del self.headteachers
        del self.schooldatas
        del self.teacherperformancedata
        del self.learnerperformancedata
        del self.inboundsms

    def test_admin_can_view_all(self):
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


        url = reverse("admin:data_headteacher_changelist")
        response = self.client.get(url)
        headteacher_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        headteacher = []
        [headteacher.append(k.emis.emis) for k in headteacher_result]
        self.assertEqual(sorted(headteacher), sorted(self.headteachers))

        url = reverse("admin:data_schooldata_changelist")
        response = self.client.get(url)
        schooldata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        schooldata = []
        [schooldata.append(k.emis.emis) for k in schooldata_result]
        self.assertEqual(sorted(schooldata), sorted(self.schooldatas))

        url = reverse("admin:data_teacherperformancedata_changelist")
        response = self.client.get(url)
        teacherperformancedata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        teacherperformancedata = []
        [teacherperformancedata.append(k.emis.emis) for k in teacherperformancedata_result]
        self.assertEqual(sorted(teacherperformancedata), sorted(self.teacherperformancedata))

        url = reverse("admin:data_learnerperformancedata_changelist")
        response = self.client.get(url)
        learnerperformancedata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        learnerperformancedata = []
        [learnerperformancedata.append(k.emis.emis) for k in learnerperformancedata_result]
        self.assertEqual(sorted(learnerperformancedata), sorted(self.learnerperformancedata))

        url = reverse("admin:sms_inboundsmsproxy_changelist")
        response = self.client.get(url)
        inboundsms_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        inboundsms = []
        [inboundsms.append(k.created_by.emis.emis) for k in inboundsms_result]
        self.assertEqual(sorted(inboundsms), sorted(self.inboundsms))



class TestDistrictAdmin1Area(TestCase):
    """
    Testing user district_admin with different district_id
    """
    fixtures = ['test_hierarchy.json', 'test_data.json', 'test_auth.json', 'test_users_district.json']

    def setUp(self):
        self.d1 = User.objects.get(username="d1")

        self.provinces = ['North Western', 'WESTERN', 'EASTERN', 'MUCHINGA', 'Luapula', 'Northern']
        self.districts = ['Solwezi', 'Mongu', 'CHIPATA', 'CHINSALI', 'Mansa', 'Mporokoso']
        self.zones = ['Kikombe', 'LUKWETA', 'MADZIMOYO', 'KALELA', 'Mbaso', 'Bweupe']
        self.schools = [3633]
        self.headteachers = [3633]
        self.schooldatas = [3633]
        self.teacherperformancedata = [3633]
        self.learnerperformancedata = [3633, 3633]
        self.inboundsms = [3633]

    def tearDown(self):
        del self.d1
        del self.provinces
        del self.districts
        del self.zones
        del self.schools
        del self.headteachers
        del self.schooldatas
        del self.teacherperformancedata
        del self.learnerperformancedata
        del self.inboundsms

    def test_d2_can_view_all(self):
        self.client.login(username=self.d1.username,
                          password="d1")

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


        url = reverse("admin:data_headteacher_changelist")
        response = self.client.get(url)
        headteacher_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        headteacher = []
        [headteacher.append(k.emis.emis) for k in headteacher_result]
        self.assertEqual(sorted(headteacher), sorted(self.headteachers))

        ## TODO - Validate failure reason
        # url = reverse("admin:data_schooldata_changelist")
        # response = self.client.get(url)
        # schooldata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        # schooldata = []
        # [schooldata.append(k.emis.emis) for k in schooldata_result]
        # self.assertEqual(sorted(schooldata), sorted(self.schooldatas))

        url = reverse("admin:data_teacherperformancedata_changelist")
        response = self.client.get(url)
        teacherperformancedata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        teacherperformancedata = []
        [teacherperformancedata.append(k.emis.emis) for k in teacherperformancedata_result]
        self.assertEqual(sorted(teacherperformancedata), sorted(self.teacherperformancedata))

        url = reverse("admin:data_learnerperformancedata_changelist")
        response = self.client.get(url)
        learnerperformancedata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        learnerperformancedata = []
        [learnerperformancedata.append(k.emis.emis) for k in learnerperformancedata_result]
        self.assertEqual(sorted(learnerperformancedata), sorted(self.learnerperformancedata))

        url = reverse("admin:sms_inboundsmsproxy_changelist")
        response = self.client.get(url)
        inboundsms_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        inboundsms = []
        [inboundsms.append(k.created_by.emis.emis) for k in inboundsms_result]
        self.assertEqual(sorted(inboundsms), sorted(self.inboundsms))


class TestDistrictAdmin2Area(TestCase):
    """
    Testing user district_admin with different district_id
    """
    fixtures = ['test_hierarchy.json', 'test_data.json', 'test_auth.json', 'test_users_district.json']

    def setUp(self):
        self.d2 = User.objects.get(username="d2")

        self.provinces = ['North Western', 'WESTERN', 'EASTERN', 'MUCHINGA', 'Luapula', 'Northern']
        self.districts = ['Solwezi', 'Mongu', 'CHIPATA', 'CHINSALI', 'Mansa', 'Mporokoso']
        self.zones = ['Kikombe', 'LUKWETA', 'MADZIMOYO', 'KALELA', 'Mbaso', 'Bweupe']
        self.schools = [2525]
        self.headteachers = [2525]
        self.schooldatas = [2525]
        self.teacherperformancedata = [2525]
        self.learnerperformancedata = [2525, 2525]
        self.inboundsms = [2525]

    def tearDown(self):
        del self.d2
        del self.provinces
        del self.districts
        del self.zones
        del self.schools
        del self.headteachers
        del self.schooldatas
        del self.teacherperformancedata
        del self.learnerperformancedata
        del self.inboundsms

    def test_d2_can_view_all(self):
        self.client.login(username=self.d2.username,
                          password="d2")

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


        url = reverse("admin:data_headteacher_changelist")
        response = self.client.get(url)
        headteacher_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        headteacher = []
        [headteacher.append(k.emis.emis) for k in headteacher_result]
        self.assertEqual(sorted(headteacher), sorted(self.headteachers))

        ## TODO - Validate failure reason
        # url = reverse("admin:data_schooldata_changelist")
        # response = self.client.get(url)
        # schooldata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        # schooldata = []
        # [schooldata.append(k.emis.emis) for k in schooldata_result]
        # self.assertEqual(sorted(schooldata), sorted(self.schooldatas))

        url = reverse("admin:data_teacherperformancedata_changelist")
        response = self.client.get(url)
        teacherperformancedata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        teacherperformancedata = []
        [teacherperformancedata.append(k.emis.emis) for k in teacherperformancedata_result]
        self.assertEqual(sorted(teacherperformancedata), sorted(self.teacherperformancedata))

        url = reverse("admin:data_learnerperformancedata_changelist")
        response = self.client.get(url)
        learnerperformancedata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        learnerperformancedata = []
        [learnerperformancedata.append(k.emis.emis) for k in learnerperformancedata_result]
        self.assertEqual(sorted(learnerperformancedata), sorted(self.learnerperformancedata))

        url = reverse("admin:sms_inboundsmsproxy_changelist")
        response = self.client.get(url)
        inboundsms_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        inboundsms = []
        [inboundsms.append(k.created_by.emis.emis) for k in inboundsms_result]
        self.assertEqual(sorted(inboundsms), sorted(self.inboundsms))


class TestAdmin3View(TestCase):
    """
    Testing user district_admin with no district_id
    """
    fixtures = ['test_hierarchy.json', 'test_data.json', 'test_auth.json', 'test_users_district.json']

    def setUp(self):
        self.d3 = User.objects.get(username="d3")

        self.provinces = ['North Western', 'WESTERN', 'EASTERN', 'MUCHINGA', 'Luapula', 'Northern']
        self.districts = ['Solwezi', 'Mongu', 'CHIPATA', 'CHINSALI', 'Mansa', 'Mporokoso']
        self.zones = ['Kikombe', 'LUKWETA', 'MADZIMOYO', 'KALELA', 'Mbaso', 'Bweupe']
        self.schools = [3633, 14090, 8682, 2064, 1774, 2525]
        self.headteachers = [2064, 3633, 2525]
        self.schooldatas = [2064, 3633, 2525]
        self.teacherperformancedata = [2064, 3633, 2525]
        self.learnerperformancedata = [2064, 2064, 3633,  3633, 2525, 2525]
        self.inboundsms = [2064, 3633, 2525]

    def tearDown(self):
        del self.d3
        del self.provinces
        del self.districts
        del self.zones
        del self.schools
        del self.headteachers
        del self.schooldatas
        del self.teacherperformancedata
        del self.learnerperformancedata
        del self.inboundsms

    def test_view_changlist(self):
        """
        The unittests allows user to view the index page for the different models.
        """
        self.client.login(username=self.d3.username,
                          password="d3")

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


        url = reverse("admin:data_headteacher_changelist")
        response = self.client.get(url)
        headteacher_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        headteacher = []
        [headteacher.append(k.emis.emis) for k in headteacher_result]
        self.assertEqual(sorted(headteacher), sorted(self.headteachers))

        url = reverse("admin:data_schooldata_changelist")
        response = self.client.get(url)
        schooldata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        schooldata = []
        [schooldata.append(k.emis.emis) for k in schooldata_result]
        self.assertEqual(sorted(schooldata), sorted(self.schooldatas))

        url = reverse("admin:data_teacherperformancedata_changelist")
        response = self.client.get(url)
        teacherperformancedata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        teacherperformancedata = []
        [teacherperformancedata.append(k.emis.emis) for k in teacherperformancedata_result]
        self.assertEqual(sorted(teacherperformancedata), sorted(self.teacherperformancedata))

        url = reverse("admin:data_learnerperformancedata_changelist")
        response = self.client.get(url)
        learnerperformancedata_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        learnerperformancedata = []
        [learnerperformancedata.append(k.emis.emis) for k in learnerperformancedata_result]
        self.assertEqual(sorted(learnerperformancedata), sorted(self.learnerperformancedata))

        url = reverse("admin:sms_inboundsmsproxy_changelist")
        response = self.client.get(url)
        inboundsms_result = response.__dict__['context_data']['cl'].__dict__['result_list']
        inboundsms = []
        [inboundsms.append(k.created_by.emis.emis) for k in inboundsms_result]
        self.assertEqual(sorted(inboundsms), sorted(self.inboundsms))
