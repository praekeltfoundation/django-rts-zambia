from django.contrib import admin
from models import (SchoolData, HeadTeacher, InboundSMS, AcademicAchievementCode,
                    TeacherPerformanceData, LearnerPerformanceData)
from actions import export_as_csv_action
from rts.utils import DistrictIdFilter, ManagePermissions



class SchoolDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "name", "classrooms", "teachers",
                    "teachers_g1", "teachers_g2", "boys_g2", "girls_g2", "created_at","created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(SchoolDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()

    def get_actions(self, request):
        actions = super(SchoolDataAdmin, self).get_actions(request)
        delete_perm = super(SchoolDataAdmin, self).has_delete_permission(request)
        return ManagePermissions(parent=self,
                                 request=request,
                                 actions=actions,
                                 delete_perm=delete_perm).remove_delete_permission()


class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ["emis", "first_name", "last_name", "msisdn", "gender", "date_of_birth", "is_zonal_head", "zonal_head_name","created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]


    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(HeadTeacherAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()

    def get_actions(self, request):
        actions = super(HeadTeacherAdmin, self).get_actions(request)
        delete_perm = super(HeadTeacherAdmin, self).has_delete_permission(request)
        return ManagePermissions(parent=self,
                                 request=request,
                                 actions=actions,
                                 delete_perm=delete_perm).remove_delete_permission()


class TeacherPerformanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "gender", "age", "years_experience", "g2_pupils_present", "g2_pupils_registered",
                    "classroom_environment_score", "t_l_materials", "pupils_materials_score",
                    "pupils_books_number", "reading_lesson", "pupil_engagement_score", "attitudes_and_beliefs",
                    "training_subtotal", "ts_number", "academic_level", "created_by", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(TeacherPerformanceDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()

    def get_actions(self, request):
        actions = super(TeacherPerformanceDataAdmin, self).get_actions(request)
        delete_perm = super(TeacherPerformanceDataAdmin, self).has_delete_permission(request)
        return ManagePermissions(parent=self,
                                 request=request,
                                 actions=actions,
                                 delete_perm=delete_perm).remove_delete_permission()
        


class LearnerPerformanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "gender", "total_number_pupils", "phonetic_awareness", "vocabulary",
                    "reading_comprehension", "writing_diction", "below_minimum_results", "minimum_results",
                    "desirable_results", "outstanding_results", "created_by", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(LearnerPerformanceDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()

    def get_actions(self, request):
        actions = super(LearnerPerformanceDataAdmin, self).get_actions(request)
        delete_perm = super(LearnerPerformanceDataAdmin, self).has_delete_permission(request)
        return ManagePermissions(parent=self,
                                 request=request,
                                 actions=actions,
                                 delete_perm=delete_perm).remove_delete_permission()


class InboundSMSAdmin(admin.ModelAdmin):
    list_display = ["message", "created_by", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file")]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(InboundSMSAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()

    def get_actions(self, request):
        actions = super(InboundSMSAdmin, self).get_actions(request)
        delete_perm = super(InboundSMSAdmin, self).has_delete_permission(request)
        return ManagePermissions(parent=self,
                                 request=request,
                                 actions=actions,
                                 delete_perm=delete_perm).remove_delete_permission()

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
admin.site.register(TeacherPerformanceData, TeacherPerformanceDataAdmin)
admin.site.register(LearnerPerformanceData, LearnerPerformanceDataAdmin)
admin.site.register(InboundSMS, InboundSMSAdmin)
admin.site.register(AcademicAchievementCode, AcademicAchievementCodeAdmin)
