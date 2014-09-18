from django.contrib import admin
from models import (SchoolData, HeadTeacher, AcademicAchievementCode,
                    SchoolMonitoringData,
                    TeacherPerformanceData, LearnerPerformanceData,
                    HeadTeacherDuplicateStore, SchoolDataDuplicateStore)

from rts.actions import export_select_fields_csv_action
from rts.utils import DistrictIdFilter, ManagePermissions
from django import forms



class SchoolDataAdmin(ManagePermissions):
    list_display = ["emis", "name", "classrooms", "teachers", "boys", "girls",
                    "teachers_g1", "teachers_g2", "boys_g2", "girls_g2", "created_by", "created_at"]
    search_fields = ["emis__emis", "emis__name"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
               fields= [
                ("emis", "EMIS"),
                ("created_at", "Created At"),
                ("created_by", "Created By"),
                ("name", "Name"),
                ("boys", "Boys"),
                ("girls", "Girls"),
                ("boys_g2", "Grade 2 Boys"),
                ("girls_g2", "Grade 2 Girls"),
                ("classrooms", "Classrooms"),
                ("teachers", "Teachers"),
                ("teachers_g2", "Grade 2 Teachers"),
                ("teachers_g1", "Grade 1 Teachers"),
               ],
               header=True
              )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(SchoolDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


class HeadTeacherAdmin(ManagePermissions):
    list_display = ["emis", "first_name", "last_name", "msisdn", "gender", "date_of_birth", "is_zonal_head", "zonal_head_name","created_at"]
    search_fields = ["emis__emis", "emis__name", "first_name", "last_name"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
               fields= [
                ("created_at", "Created At"),
                ("first_name", "First Name"),
                ("last_name", "Last Name"),
                ("msisdn", "MSISDN"),
                ("gender", "Gender"),
                ("date_of_birth", "Date of Birth"),
                ("is_zonal_head", "Is Zonal Head"),
                ("zonal_head_name", "Zonal Head Name"),
                ("emis", "EMIS"),
               ],
               header=True
              )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(HeadTeacherAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


class SchoolMonitoringDataAdmin(ManagePermissions):
    list_display = ["emis", "school_improvement_plan", "no_improvement_plan", "teaching",
                    "learner_assessment", "learning_materials", "learner_attendance",
                    "instructional_time", "struggling_learners", "support_ovcs",
                    "classroom_observation_ht", "learner_performance_ht", "summary_worksheet",
                    "created_by", "created_at"]
    search_fields = ["emis__emis", "emis__name"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
                fields= [
                 ("emis", "EMIS"),
                 ("created_at", "Created At"),
                 ("created_by", "Created By"),
                 ("school_improvement_plan", "School Learner Performance Improvement Plan"),
                 ("no_improvement_plan", "Reason for not seeing Improvement Plan"),
                 ("teaching", "Activity for Improving Teaching"),
                 ("learner_assessment", "Activity for Improving Learner Assessment"),
                 ("learning_materials", "Acquiring Learning Materials"),
                 ("learner_attendance", "Activity for Improving Learner Attendance"),
                 ("instructional_time", "Activity for Improving Instructional Time"),
                 ("struggling_learners", "Extra Support for Struggling Learners"),
                 ("support_ovcs", "Activity to Support OVCs"),
                 ("classroom_observation_ht", "ClassRoom Observation Results by Head Teacher"),
                 ("learner_performance_ht", "Learner Performance Assessments by Head Teacher"),
                 ("summary_worksheet", "Summary Worksheet Accurate by Head Teacher"),
                ],
                header= True
               )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(SchoolMonitoringDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


class TeacherPerformanceDataAdmin(ManagePermissions):
    list_display = ["emis", "gender", "age", "years_experience", "g2_pupils_present", "g2_pupils_registered",
                    "classroom_environment_score", "t_l_materials", "pupils_materials_score",
                    "pupils_books_number", "reading_lesson", "pupil_engagement_score", "attitudes_and_beliefs",
                    "training_subtotal", "ts_number", "reading_assessment", "reading_total", "academic_level",
                    "created_by", "created_at"]
    search_fields = ["emis__emis", "emis__name"]
    raw_id_fields = ("created_by",)
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
               fields= [
                ("emis", "EMIS"),
                ("created_at", "Created At"),
                ("created_by", "Created By"),
                ("gender", "Gender"),
                ("age", "Age"),
                ("ts_number", "TS Number"),
                ("academic_level", "Academic Level"),
                ("years_experience", "Years of Experience"),
                ("g2_pupils_registered", "Grade 2 Pupils Registered"),
                ("g2_pupils_present", "Grade 2 Pupils Present"),
                ("classroom_environment_score", "Classroom Environment Score"),
                ("pupils_books_number", "Pupils Book Number"),
                ("pupils_materials_score", "Pupils Materials Score"),
                ("t_l_materials", "T L Materials"),
                ("reading_lesson", "Reading lesson"),
                ("pupil_engagement_score", "Pupil Engagement Score"),
                ("attitudes_and_beliefs", "Attitudes And Beliefs"),
                ("training_subtotal", "Training Subtotal"),
                ("reading_assessment", "Reading Assessment"),
                ("reading_total", "Reading Total"),
               ],
               header=True
              )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(TeacherPerformanceDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


class LearnerPerformanceDataAdmin(ManagePermissions):
    list_display = ["emis", "gender", "total_number_pupils", "phonetic_awareness", "vocabulary",
                    "reading_comprehension", "writing_diction", "below_minimum_results", "minimum_results",
                    "desirable_results", "outstanding_results", "created_by", "created_at"]
    search_fields = ["emis__emis", "emis__name"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
               fields= [
                ("emis", "EMIS"),
                ("created_by", "Created By"),
                ("created_at", "Created At"),
                ("gender", "Gender"),
                ("total_number_pupils", "Total Number of Pupils"),
                ("phonetic_awareness", "Phonetic Awareness"),
                ("writing_diction", "Writing Diction"),
                ("reading_comprehension", "Reading Comprehension"),
                ("vocabulary", "Vocabulary"),
                ("outstanding_results", "Outstanding Results"),
                ("desirable_results", "Desirable Results"),
                ("minimum_results", "Minimum Results"),
                ("below_minimum_results", "Below Minimum Results"),
               ],
               header=True
              )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(LearnerPerformanceDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


class AcademicAchievementCodeAdmin(admin.ModelAdmin):
    list_display = ["id", "achievement"]
    actions = None

    def has_add_permission(self, request):
        return False

    def __init__(self, *args, **kwargs):
        super(AcademicAchievementCodeAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )


class SchoolDataDuplicateStoreAdmin(admin.ModelAdmin):
    list_display = ["id", "origin_id", "emis", "name", "classrooms", "teachers",
                    "teachers_g1", "teachers_g2", "boys_g2", "girls_g2", "created_by", "created_at"]


class HeadTeacherDuplicateStoreAdmin(ManagePermissions):
    list_display = ["id", "origin_id", "emis", "first_name", "last_name", "msisdn", "gender", "date_of_birth", "is_zonal_head", "zonal_head_name","created_at"]

admin.site.register(SchoolData, SchoolDataAdmin)
admin.site.register(HeadTeacher, HeadTeacherAdmin)
admin.site.register(SchoolMonitoringData, SchoolMonitoringDataAdmin)
admin.site.register(TeacherPerformanceData, TeacherPerformanceDataAdmin)
admin.site.register(LearnerPerformanceData, LearnerPerformanceDataAdmin)
admin.site.register(AcademicAchievementCode, AcademicAchievementCodeAdmin)

admin.site.register(SchoolDataDuplicateStore, SchoolDataDuplicateStoreAdmin)
admin.site.register(HeadTeacherDuplicateStore, HeadTeacherDuplicateStoreAdmin)
