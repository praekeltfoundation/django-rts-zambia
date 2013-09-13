from django.contrib import admin
from sms.models import SendSMS, SMSDatabase


class SendSMSAdmin(admin.ModelAdmin):
    pass


class SMSDatabaseAdmin(admin.ModelAdmin):
    pass


admin.site.register(SendSMS, SendSMSAdmin)
admin.site.register(SMSDatabase, SMSDatabaseAdmin)
