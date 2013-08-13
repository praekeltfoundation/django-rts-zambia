from django.contrib import admin
from models import (SchoolData, HeadTeacher, TeacherPerfomanceData)


class SchoolDataAdmin(admin.ModelAdmin):
    list_display = ["emis"]


class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ["emis", "first_name", "last_name", "msisdn"]

class TeacherPerfomanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "created_by"]


admin.site.register(SchoolData, SchoolDataAdmin)
admin.site.register(HeadTeacher, HeadTeacherAdmin)
admin.site.register(TeacherPerfomanceData, TeacherPerfomanceDataAdmin)
