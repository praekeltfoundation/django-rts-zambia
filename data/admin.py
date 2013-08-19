from django.contrib import admin
from models import (SchoolData, HeadTeacher, InboundSMS, AcademicAchievementCode,
                    TeacherPerfomanceData, LearnerPerfomanceData)
from actions import export_as_csv_action



class SchoolDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(SchoolDataAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(emis__zone__district=request.user.userdistrict.district_id)


class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ["id", "emis", "first_name", "last_name", "msisdn", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]


    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(HeadTeacherAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        print request.user.userdistrict.district_id;
        print dir(request.user.userdistrict);
        return qs.filter(emis__zone__district=request.user.userdistrict.district_id)

class TeacherPerfomanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "created_by", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(TeacherPerfomanceDataAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(emis__zone__district=request.user.userdistrict.district_id)


class LearnerPerfomanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "created_by", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(LearnerPerfomanceDataAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(emis__zone__district=request.user.userdistrict.district_id)


class InboundSMSAdmin(admin.ModelAdmin):
    list_display = ["message", "created_by", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(InboundSMSAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by__emis__zone__district=request.user.userdistrict.district_id)


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
