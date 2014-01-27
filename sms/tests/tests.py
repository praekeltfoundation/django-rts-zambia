# DJango
from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Project
from sms.models import SendSMS, SMSZones, TempSMSZones
from sms.tasks import send_sms, task_query_zone
from hierarchy.models import Zone, District
from users.models import UserDistrict


class TestAdminCreation(TestCase):
    fixtures = ['test_sms_hierarchy_upload.json', 'test_sms_auth.json', 'test_sms_user_district.json']

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS = True,
                       CELERY_ALWAYS_EAGER = True,
                       BROKER_BACKEND = 'memory',)
    def setUp(self):
        self.d1 = User.objects.get(username="d1")
        zones_all = Zone.objects.filter(district=self.d1.userdistrict.district_id).all()
        self.d1_zones_id = [obj.id for obj in zones_all]
        self.client.logout()

    def test_hierarchy_loaded(self):
        """
        Test to see if the zone was loaded
        """
        zone = Zone.objects.get(id=1)
        self.assertEqual(zone.id, 1)

    def test_send_single_sms_zone(self):
        """
        Testing posted SMS
        """
        self.client.login(username=self.d1.username,
                          password="d1")
        url = reverse("admin:sms_sendsms_add")
        data = {"sms": "Sending the SMS 1",
                'tempsmszones_set-INITIAL_FORMS': 0,
                'tempsmszones_set-TOTAL_FORMS': 1,
                'tempsmszones_set-MAX_NUM_FORMS':  u'',
                'tempsmszones_set-0-all': [u'on']
                }
        self.client.post(url, data=data)
        sendsms = SendSMS.objects.get(sms="Sending the SMS 1")
        self.assertEqual(sendsms.sms, "Sending the SMS 1")
        sms_zone = SMSZones.objects.all()
        self.assertEqual(sorted(self.d1_zones_id),
                         sorted([obj.zone_id for obj in sms_zone]))

    # def test_send_all_validation_sms_zone(self):
    #     """
    #     Testing posted SMS
    #     """
    #     self.client.login(username=self.d1.username,
    #                       password="d1")
    #     url = reverse("admin:sms_sendsms_add")
    #     data = {"sms": "Sending the SMS",
    #             'tempsmszones_set-INITIAL_FORMS': 0,
    #             'tempsmszones_set-TOTAL_FORMS': 1,
    #             'tempsmszones_set-MAX_NUM_FORMS':  u'',
    #             'tempsmszones_set-0-all': [u'on'],
    #             'tempsmszones_set-0-139': [u'on'],
    #             'tempsmszones_set-0-140': [u'on'],
    #             'tempsmszones_set-0-141': [u'on'],
    #             'tempsmszones_set-0-142': [u'on']

    #             }


    #     response = self.client.post(url, data=data)
    #     self.assertIn("Choose all or specific zones not both",
    #                   response.context_data["errors"])


    # def test_send_specific_zones(self):
    #     """
    #     Testing posted SMS
    #     """
    #     self.client.login(username=self.d1.username,
    #                       password="d1")
    #     url = reverse("admin:sms_sendsms_add")
    #     data = {"sms": "Sending the SMS 3",
    #             'tempsmszones_set-INITIAL_FORMS': 0,
    #             'tempsmszones_set-TOTAL_FORMS': 1,
    #             'tempsmszones_set-MAX_NUM_FORMS':  u'',
    #             'tempsmszones_set-0-139': [u'on'],
    #             'tempsmszones_set-0-140': [u'on'],
    #             'tempsmszones_set-0-141': [u'on'],
    #             'tempsmszones_set-0-142': [u'on']

    #             }
    #     self.client.post(url, data=data)
    #     sendsms = SendSMS.objects.get(sms="Sending the SMS 3")
    #     self.assertEqual(sendsms.sms, "Sending the SMS 3")
    #     sms_zone = SMSZones.objects.all()
    #     self.assertEqual(sorted([139, 140, 141, 142]),
    #                      sorted([obj.zone_id for obj in sms_zone]))



class TestSendSMSToDistrict(TestCase):
    fixtures = ['test_hierarchy.json', 'test_data.json']

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

    def test_render_sms_add_admin_view_logged_in_as_district_admin_redirects_to_add_view(self):
        self.client.login(username=self.district_admin.username,
                          password="pass123")
        response = self.client.get(self.sms_add_view, follow=True)
        self.assertEquals(response.request["PATH_INFO"], self.sms_add_view)

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

        self.assertEquals(SendSMS.objects.all()[0].sms, "SMS MESSAGE")
        self.assertEquals(sorted(District.objects.values_list("name", flat=True)),
                          sorted(SendSMS.objects.values_list("district__name", flat=True)))

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

        self.assertEquals(district.name,
                          SendSMS.objects.all()[0].district.name)

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
                          'Choose all or specific zones not both')
        self.assertEquals(response.request["PATH_INFO"], self.sms_district_view)
