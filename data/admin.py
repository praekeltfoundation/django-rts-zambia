from django.contrib import admin
from models import (SchoolData, HeadTeacher, InboundSMS)
from actions import export_as_csv_action


class SchoolDataAdmin(admin.ModelAdmin):
    list_display = ["emis"]


class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ["emis", "first_name", "last_name", "msisdn"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]


class InboundSMSAdmin(admin.ModelAdmin):
    list_display = ["message", "created_by", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]


admin.site.register(SchoolData, SchoolDataAdmin)
admin.site.register(HeadTeacher, HeadTeacherAdmin)
admin.site.register(InboundSMS, InboundSMSAdmin)
