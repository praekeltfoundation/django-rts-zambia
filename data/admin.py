from django.contrib import admin
from models import (SchoolData, HeadTeacher, TeacherPerfomanceData, LearnerPerfomanceData)


class SchoolDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "created_at"]


class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ["emis", "first_name", "last_name", "msisdn", "created_at"]


class TeacherPerfomanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "created_by", "created_at"]


class LearnerPerfomanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "created_by", "created_at"]


admin.site.register(SchoolData, SchoolDataAdmin)
admin.site.register(HeadTeacher, HeadTeacherAdmin)
admin.site.register(TeacherPerfomanceData, TeacherPerfomanceDataAdmin)
admin.site.register(LearnerPerfomanceData, LearnerPerfomanceDataAdmin)
