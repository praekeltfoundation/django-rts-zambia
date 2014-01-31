# DJango
from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Project
from sms.models import SendSMS, SMSZones
from hierarchy.models import Zone, District
from users.models import UserDistrict


class TestAdminCreation(TestCase):
    fixtures = ['test_sms_hierarchy_upload.json', 'test_sms_auth.json', 'test_sms_user_district.json']


    def setUp(self):
        self.d1 = User.objects.get(username="d1")
        zones_all = Zone.objects.filter(district=self.d1.userdistrict.district_id).all()
        self.d1_zones_id = [obj.id for obj in zones_all]
        self.client.logout()

@override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS = True,
                       CELERY_ALWAYS_EAGER = True,
                       BROKER_BACKEND = 'memory',)
class TestSendSMSToZone(TestCase):
    fixtures = ['test_hierarchy.json', 'test_data.json', 'test_sms_hierarchy_upload.json', 'test_sms_auth.json', 'test_sms_user_district.json']

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS = True,
                       CELERY_ALWAYS_EAGER = True,
                       BROKER_BACKEND = 'memory',)
    def setUp(self):
        # Specific District Admin
        # self.d1 = User.objects.get(username="d1")
        # zones_all = Zone.objects.filter(district=self.d1.userdistrict.district_id).all()
        # self.d1_zones_id = [obj.id for obj in zones_all]

        self.rts_staff = User.objects.create_user('rts_staff',
                                               'rts_staff@thebeatles.com',
                                               'pass123')
        self.rts_staff.is_staff = True
        self.rts_staff.save()

        self.district_admin = User.objects.create_user('district_admin',
                                                       'district_admin@thebeatles.com',
                                                       'pass123')
        self.district_admin.is_staff = True
        self.district_admin.save()

        userdistrict, _ = UserDistrict.objects.get_or_create(user=self.district_admin,
                                                             district=District.objects.get(name="Mporokoso"))

        self.sms_zones_view = reverse("admin:sms_sendsms_zones_view")
        self.sms_districts_view = reverse("admin:sms_sendsms_districts_view")
        self.sms_add_view = reverse("admin:sms_sendsms_add")
        self.admin_index = reverse("admin:index")

        self.provinces = ['North Western', 'WESTERN', 'EASTERN', 'MUCHINGA', 'Luapula', 'Northern']
        self.districts = ['Solwezi', 'Mongu', 'CHIPATA', 'CHINSALI', 'Mansa', 'Mporokoso']
        self.zones = ['Kikombe', 'LUKWETA', 'MADZIMOYO', 'KALELA', 'Mbaso', 'Bweupe']
        self.schools = [3633, 14090, 8682, 2064, 1774, 2525]
        self.headteachers = [2064, 3633, 2525]
        self.schooldatas = [2064, 3633, 2525]
        self.teacherperformancedata = [2064, 3633, 2525]
        self.learnerperformancedata = [2064, 2064, 3633,  3633, 2525, 2525]
        self.inboundsms = [2064, 3633, 2525]

    def test_authorized_direct_access_to_districts_sms_view_as_district_admin_is_ok(self):
        self.client.login(username=self.district_admin.username,
                          password="pass123")
        response = self.client.get(self.sms_zones_view, follow=True)

        self.assertTemplateUsed(response, "admin/sms/sendsms/zones_view.html")
        self.assertEquals(response.request["PATH_INFO"], self.sms_zones_view)
        self.assertIn("zone_form", response.context)

        zone_ids = Zone.objects.filter(district__userdistrict__user=self.district_admin).values_list('id', flat=True)
        field_names = [unicode(ids) for ids in zone_ids]
        field_names  = field_names + ["send_to_all", "sms"]

        self.assertEquals(sorted(response.context["zone_form"].fields.keys()),
                          sorted(field_names))

    def test_unauthorized_direct_access_to_sms_districts_redirects_to_admin(self):
        self.client.login(username=self.rts_staff.username,
                          password="pass123")
        response = self.client.get(self.sms_zones_view, follow=True)
        self.assertEquals(response.request["PATH_INFO"], self.admin_index)

    def test_render_sms_add_admin_view_logged_in_as_district_admin_redirects_to_zones_view(self):
        self.client.login(username=self.district_admin.username,
                          password="pass123")
        response = self.client.get(self.sms_add_view, follow=True)
        self.assertEquals(response.request["PATH_INFO"], self.sms_zones_view)

    def test_render_sms_add_admin_view_logged_in_as_rts_staff_redirects_to_districts_view(self):
        self.client.login(username=self.rts_staff.username,
                          password="pass123")
        response = self.client.get(self.sms_districts_view, follow=True)
        self.assertEquals(response.request["PATH_INFO"], self.sms_districts_view)


    def test_post_data_for_sms_to_zone_send_to_all(self):
        self.client.login(username=self.district_admin.username,
                          password="pass123")
        data = {"send_to_all": True,
                "sms": "SMS MESSAGE"}
        response = self.client.post(self.sms_zones_view,
                                    data=data,
                                    follow=True)
        self.assertEquals(response.request["PATH_INFO"], reverse("admin:sms_sendsms_changelist"))
        self.assertContains(response, "The messages have been sent")

        send_sms_obj = SendSMS.objects.all()[0]
        # Checking that the sms is the same was was sent
        self.assertEquals(send_sms_obj.sms, "SMS MESSAGE")

        # Making sure that all districts were sent to
        self.assertEquals(self.district_admin.userdistrict.district.name,
                          send_sms_obj.district.name)

        # Checking if the sent_to_all field is true
        (self.assertTrue(item) for item in SendSMS.objects.values_list("sent_to_all", flat=True))

        # Making sure that all zones were sent to
        self.assertEquals(sorted(Zone.objects.filter(district__userdistrict__user=self.district_admin).values_list('name', flat=True)),
                          sorted(SMSZones.objects.values_list("zone__name", flat=True)))


    def test_post_data_for_sms_to_with_one_zone(self):
        self.client.login(username=self.district_admin.username,
                          password="pass123")
        data = {"1": True,
                "sms": "SMS MESSAGE"}
        response = self.client.post(self.sms_zones_view,
                                    data=data,
                                    follow=True)
        self.assertEquals(response.request["PATH_INFO"], reverse("admin:sms_sendsms_changelist"))
        self.assertContains(response, "The messages have been sent")

        send_sms_obj = SendSMS.objects.all()[0]

        self.assertEquals(SendSMS.objects.all()[0].sms, "SMS MESSAGE")

        # Making sure that all districts were sent to
        self.assertEquals(self.district_admin.userdistrict.district.name,
                          send_sms_obj.district.name)

        # Checking if the sent_to_all field is true
        (self.assertFalse(item) for item in SendSMS.objects.values_list("sent_to_all", flat=True))

        smsed_zones = SMSZones.objects.all()
        self.assertEquals(smsed_zones.count(), 1)
        self.assertEquals(Zone.objects.get(id=1).name,
                          smsed_zones[0].zone.name)


    def test_validation_for_send_to_all_and_another_zone_selected(self):
        self.client.login(username=self.district_admin.username,
                          password="pass123")
        data = {"1": True,
                "send_to_all": True,
                "sms": "SMS MESSAGE"}

        response = self.client.post(self.sms_zones_view,
                                    data=data,
                                    follow=True)
        self.assertEquals(response.context["zone_form"].errors["__all__"][0],
                          "Choose all or specific zones not both")
        self.assertEquals(response.request["PATH_INFO"], self.sms_zones_view)

    def test_validation_for_for_nothing_is_selected(self):
        self.client.login(username=self.district_admin.username,
                          password="pass123")
        data = {"sms": "SMS MESSAGE"}

        response = self.client.post(self.sms_zones_view,
                                    data=data,
                                    follow=True)
        self.assertEquals(response.context["zone_form"].errors["__all__"][0],
                          "Please choose an option")
        self.assertEquals(response.request["PATH_INFO"], self.sms_zones_view)



class TestSendSMSToDistrict(TestCase):
    fixtures = ['test_hierarchy.json', 'test_data.json']

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS = True,
                       CELERY_ALWAYS_EAGER = True,
                       BROKER_BACKEND = 'memory',)
    def setUp(self):
        self.rts_staff = User.objects.create_user('rts_staff',
                                               'rts_staff@thebeatles.com',
                                               'pass123')
        self.rts_staff.is_staff = True
        self.rts_staff.save()

        self.district_admin = User.objects.create_user('district_admin',
                                               'district_admin@thebeatles.com',
                                               'pass123')
        self.district_admin.is_staff = True
        self.district_admin.save()

        userdistrict, _ = UserDistrict.objects.get_or_create(user=self.district_admin,
                                                             district=District.objects.get(name="Mporokoso"))

        self.sms_district_view = reverse("admin:sms_sendsms_districts_view")
        self.sms_zone_view = reverse("admin:sms_sendsms_zones_view")
        self.sms_add_view = reverse("admin:sms_sendsms_add")
        self.admin_index = reverse("admin:index")

        self.provinces = ['North Western', 'WESTERN', 'EASTERN', 'MUCHINGA', 'Luapula', 'Northern']
        self.districts = ['Solwezi', 'Mongu', 'CHIPATA', 'CHINSALI', 'Mansa', 'Mporokoso']
        self.zones = ['Kikombe', 'LUKWETA', 'MADZIMOYO', 'KALELA', 'Mbaso', 'Bweupe']
        self.schools = [3633, 14090, 8682, 2064, 1774, 2525]
        self.headteachers = [2064, 3633, 2525]
        self.schooldatas = [2064, 3633, 2525]
        self.teacherperformancedata = [2064, 3633, 2525]
        self.learnerperformancedata = [2064, 2064, 3633,  3633, 2525, 2525]
        self.inboundsms = [2064, 3633, 2525]

    def test_authorized_direct_access_to_districts_sms_view_as_rts_staff_is_ok(self):
        self.client.login(username=self.rts_staff.username,
                          password="pass123")
        response = self.client.get(self.sms_district_view, follow=True)
        self.assertEquals(response.request["PATH_INFO"], self.sms_district_view)
        self.assertIn("district_form", response.context)

        district_ids = District.objects.values_list('id', flat=True)
        field_names = [unicode(ids) for ids in district_ids]
        field_names  = field_names + ["send_to_all", "sms"]

        self.assertEquals(sorted(response.context["district_form"].fields.keys()),
                          sorted(field_names))

    def test_unauthorized_direct_access_to_sms_districts_redirects_to_admin(self):
        self.client.login(username=self.district_admin.username,
                          password="pass123")
        response = self.client.get(self.sms_district_view, follow=True)
        self.assertEquals(response.request["PATH_INFO"], self.admin_index)

    def test_render_sms_add_admin_view_logged_in_as_district_admin_redirects_to_zones_view(self):
        self.client.login(username=self.district_admin.username,
                          password="pass123")
        response = self.client.get(self.sms_add_view, follow=True)
        self.assertEquals(response.request["PATH_INFO"], self.sms_zone_view)

    def test_render_sms_add_admin_view_logged_in_as_rts_staff_redirects_to_districts_view(self):
        self.client.login(username=self.rts_staff.username,
                          password="pass123")
        response = self.client.get(self.sms_add_view, follow=True)
        self.assertEquals(response.request["PATH_INFO"], self.sms_district_view)


    def test_post_data_for_sms_to_selected_district_with_send_to_all(self):
        self.client.login(username=self.rts_staff.username,
                          password="pass123")
        data = {"send_to_all": True,
                "sms": "SMS MESSAGE"}
        response = self.client.post(self.sms_district_view,
                                    data=data,
                                    follow=True)
        self.assertEquals(response.request["PATH_INFO"], reverse("admin:sms_sendsms_changelist"))
        self.assertContains(response, "The messages have been sent")

        # Checking that the sms is the same was was sent
        self.assertEquals(SendSMS.objects.all()[0].sms, "SMS MESSAGE")

        # Making sure that all districts were sent to
        self.assertEquals(sorted(District.objects.values_list("name", flat=True)),
                          sorted(SendSMS.objects.values_list("district__name", flat=True)))

        # Checking if the sent_to_all field is true
        (self.assertTrue(item) for item in SendSMS.objects.values_list("sent_to_all", flat=True))

        # Making sure that all zones were sent to
        self.assertEquals(sorted(District.objects.values_list("zone__name", flat=True)),
                          sorted(SMSZones.objects.values_list("zone__name", flat=True)))


    def test_post_data_for_sms_to_selected_district_with_one_district(self):
        self.client.login(username=self.rts_staff.username,
                          password="pass123")
        data = {"1": True,
                "sms": "SMS MESSAGE"}
        response = self.client.post(self.sms_district_view,
                                    data=data,
                                    follow=True)
        self.assertEquals(response.request["PATH_INFO"], reverse("admin:sms_sendsms_changelist"))
        self.assertContains(response, "The messages have been sent")
        district = District.objects.get(id=1)

        self.assertEquals(SendSMS.objects.all()[0].sms, "SMS MESSAGE")

        # Making sure that the only the required district was sent to
        self.assertEquals(sorted([district.name]),
                          sorted(SendSMS.objects.values_list("district__name", flat=True)))

        # Checking if the sent_to_all field is true
        (self.assertTrue(item) for item in SendSMS.objects.values_list("sent_to_all", flat=True))

        district_zones = district.zone_set.all()
        self.assertEquals(sorted([zone.name for zone in district_zones]),
                          sorted(SMSZones.objects.values_list("zone__name", flat=True)))


    def test_validation_for_send_to_all_and_another_district_selected(self):
        self.client.login(username=self.rts_staff.username,
                          password="pass123")
        data = {"1": True,
                "send_to_all": True,
                "sms": "SMS MESSAGE"}

        response = self.client.post(self.sms_district_view,
                                    data=data,
                                    follow=True)
        self.assertEquals(response.context["district_form"].errors["__all__"][0],
                          'Choose all or specific districts not both')
        self.assertEquals(response.request["PATH_INFO"], self.sms_district_view)


    def test_validation_for_for_nothing_is_selected(self):
        self.client.login(username=self.rts_staff.username,
                          password="pass123")
        data = {"sms": "SMS MESSAGE"}

        response = self.client.post(self.sms_district_view,
                                    data=data,
                                    follow=True)
        self.assertEquals(response.context["district_form"].errors["__all__"][0],
                          "Please choose an option")
        self.assertEquals(response.request["PATH_INFO"], self.sms_district_view)
