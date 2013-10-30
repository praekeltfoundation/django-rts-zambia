from django.db import models
from django.contrib.auth.models import User


class SendSMS(models.Model):
    sms = models.CharField(max_length=160*4)
    total_sent = models.IntegerField(null=True)
    replies = models.IntegerField(null=True)
    user = models.ForeignKey(User)
    district = models.ForeignKey('hierarchy.District')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.sms

    class Meta:
        verbose_name_plural = "Send SMS's"

    def total_sent_messages(self):
        return self.total_sent

    def created_by(self):
        return self.user

    total_sent_messages.short_description = "Total Sent"
    created_by.short_description = "Created By"


class SMSZones(models.Model):
    zone = models.ForeignKey('hierarchy.Zone')
    send_sms = models.ForeignKey(SendSMS)
    num_sent = models.IntegerField(null=True)

    def __unicode__(self):
        return "%s" % self.send_sms

    class Meta:
        verbose_name = "SMS Zone"
        verbose_name_plural = "SMS Zone"


class TempSMSZones(models.Model):
    temp_sms = models.ForeignKey(SendSMS, verbose_name=u'SMSing')

    def __unicode__(self):
        return "%s" % self.temp_sms

    class Meta:
        verbose_name = "SMS To Zone"
        verbose_name_plural = "SMS To Zones"