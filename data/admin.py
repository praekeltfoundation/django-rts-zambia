from django.contrib import admin
from models import (SchoolData, HeadTeacher)


class SchoolDataAdmin(admin.ModelAdmin):
    list_display = ["emis"]


class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ["emis", "first_name", "last_name", "msisdn"]


admin.site.register(SchoolData, SchoolDataAdmin)
admin.site.register(HeadTeacher, HeadTeacherAdmin)
