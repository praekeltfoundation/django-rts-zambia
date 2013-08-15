from django.contrib import admin
from models import (SchoolData, HeadTeacher, InboundSMS, AcademicAchievementCode,
                    TeacherPerfomanceData, LearnerPerfomanceData)
from actions import export_as_csv_action



class SchoolDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "created_at"]


class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ["emis", "first_name", "last_name", "msisdn", "created_at"]


class TeacherPerfomanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "created_by", "created_at"]


class LearnerPerfomanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "created_by", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]


class InboundSMSAdmin(admin.ModelAdmin):
    list_display = ["message", "created_by", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]

class AcademicAchievementCodeAdmin(admin.ModelAdmin):
    list_display = ["id", "achievement"]
    actions = None

    def has_add_permission(self, request):
        return False

    def __init__(self, *args, **kwargs):
        super(AcademicAchievementCodeAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )


admin.site.register(SchoolData, SchoolDataAdmin)
admin.site.register(HeadTeacher, HeadTeacherAdmin)
admin.site.register(TeacherPerfomanceData, TeacherPerfomanceDataAdmin)
admin.site.register(LearnerPerfomanceData, LearnerPerfomanceDataAdmin)
admin.site.register(InboundSMS, InboundSMSAdmin)
admin.site.register(AcademicAchievementCode, AcademicAchievementCodeAdmin)
