from django.contrib import admin
from models import (SchoolData, HeadTeacher)


class SchoolDataAdmin(admin.ModelAdmin):
    list_display = ["EMIS_id_school_data"]


class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ["EMIS_id_header_teacher", "first_name", "last_name", "mobile_number"]


admin.site.register(SchoolData, SchoolDataAdmin)
admin.site.register(HeadTeacher, HeadTeacherAdmin)
