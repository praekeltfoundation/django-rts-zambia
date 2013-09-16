from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
import json
import random
from sms.models import SendSMS, SMSZones, TempSMSZones
from sms.tasks import send_sms, task_query_zone
from hierarchy.models import Zone


class TestAdminCreation(TestCase):
    fixtures = ['test_sms_hierarchy_upload.json', 'test_sms_auth.json', 'test_sms_user_district.json']

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS = True,
                       CELERY_ALWAYS_EAGER = True,
                       BROKER_BACKEND = 'memory',)
    def setUp(self):
        self.d1 = User.objects.get(username="d1")
        zones_all = Zone.objects.filter(district=self.d1.userdistrict.district_id).all()
        self.d1_zones_id = [obj.id for obj in zones_all]

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
        data = {"sms": "Sending the SMS",
                'tempsmszones_set-INITIAL_FORMS': 0,
                'tempsmszones_set-TOTAL_FORMS': 1,
                'tempsmszones_set-MAX_NUM_FORMS':  u'',
                'tempsmszones_set-0-all': [u'on']
                }
        self.client.post(url, data=data)
        send_sms = SendSMS.objects.get(id=1)
        self.assertEqual(send_sms.sms, "Sending the SMS")
        sms_zone = SMSZones.objects.all()
        self.assertEqual(sorted(self.d1_zones_id),
                         sorted([obj.zone_id for obj in sms_zone]))
        # import pdb; pdb.set_trace()

    def test_send_all_validation_sms_zone(self):
        """
        Testing posted SMS
        """
        self.client.login(username=self.d1.username,
                          password="d1")
        url = reverse("admin:sms_sendsms_add")
        data = {"sms": "Sending the SMS",
                'tempsmszones_set-INITIAL_FORMS': 0,
                'tempsmszones_set-TOTAL_FORMS': 1,
                'tempsmszones_set-MAX_NUM_FORMS':  u'',
                'tempsmszones_set-0-all': [u'on'],
                'tempsmszones_set-0-139': [u'on'],
                'tempsmszones_set-0-140': [u'on'],
                'tempsmszones_set-0-141': [u'on'],
                'tempsmszones_set-0-142': [u'on']

                }
        response = self.client.post(url, data=data)
        self.assertIn("Choose all or specific zones not both",
                      response.context_data["errors"])


    def test_send_specific_zones(self):
        """
        Testing posted SMS
        """
        self.client.login(username=self.d1.username,
                          password="d1")
        url = reverse("admin:sms_sendsms_add")
        data = {"sms": "Sending the SMS",
                'tempsmszones_set-INITIAL_FORMS': 0,
                'tempsmszones_set-TOTAL_FORMS': 1,
                'tempsmszones_set-MAX_NUM_FORMS':  u'',
                'tempsmszones_set-0-139': [u'on'],
                'tempsmszones_set-0-140': [u'on'],
                'tempsmszones_set-0-141': [u'on'],
                'tempsmszones_set-0-142': [u'on']

                }
        self.client.post(url, data=data)
        send_sms = SendSMS.objects.get(id=1)
        self.assertEqual(send_sms.sms, "Sending the SMS")
        sms_zone = SMSZones.objects.all()
        self.assertEqual(sorted([139, 140, 141, 142]),
                         sorted([obj.zone_id for obj in sms_zone]))


