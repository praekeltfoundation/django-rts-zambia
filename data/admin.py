from django.contrib import admin
from models import (SchoolData, HeadTeacher, AcademicAchievementCode,
                    SchoolMonitoringData, DistrictAdminUser,
                    TeacherPerformanceData, LearnerPerformanceData,
                    HeadTeacherDuplicateStore, SchoolDataDuplicateStore)
from users.models import UserDistrict

from rts.actions import export_select_fields_csv_action
from rts.utils import DistrictIdFilter, ManagePermissions
from django import forms



class SchoolDataAdmin(ManagePermissions):
    list_display = ["emis", "name", "classrooms", "teachers", "boys", "girls",
                    "teachers_g1", "teachers_g2", "boys_g2", "girls_g2", "created_by", "created_at"]
    search_fields = ["emis__emis", "emis__name"]
    raw_id_fields = ("created_by",)
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


class DistrictAdminUserAdmin(ManagePermissions):
    list_display = ["first_name", "last_name", "date_of_birth", "district", "id_number", "created_at"]
    search_fields = ["first_name", "last_name"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
               fields= [
                ("created_at", "Created At"),
                ("first_name", "First Name"),
                ("last_name", "Last Name"),
                ("district", "District"),
                ("id_number", "ID Number"),
                ("date_of_birth", "Date of Birth"),
               ],
               header=True
              )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(DistrictAdminUserAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


class SchoolMonitoringDataAdmin(ManagePermissions):
    list_display = ["emis", "see_lpip", "teaching",
                    "learner_assessment", "learning_materials", "learner_attendance",
                    "reading_time", "struggling_learners", "g2_observation_results",
                    "ht_feedback", "submitted_classroom", "gala_sheets", "summary_worksheet",
                    "ht_feedback_literacy", "submitted_gala", "talking_wall",
                    "created_by", "created_at"]
    search_fields = ["emis__emis", "emis__name"]
    raw_id_fields = ("created_by",)
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
                fields= [
                 ("emis", "EMIS"),
                 ("created_at", "Created At"),
                 ("created_by", "Created By"),
                 ("school_improvement_plan", "Saw School Learner Performance Improvement Plan"),
                 ("teaching", "Activity for Improving Teaching"),
                 ("learner_assessment", "Activity for Improving Learner Assessment"),
                 ("learning_materials", "Activity for Acquiring Learning Materials"),
                 ("learner_attendance", "Activity for Improving Learner Attendance"),
                 ("reading_time", "Activity for Improving Reading Time"),
                 ("struggling_learners", "Extra Support for Struggling Learners"),
                 ("g2_observation_results", "Saw Grade 2 Reading Lesson Observation Results"),
                 ("ht_feedback", "Head Teacher Feedback"),
                 ("submitted_classroom", "Submitted Classroom Observation Results"),
                 ("gala_sheets", "Saw GALA stimulus sheets"),
                 ("summary_worksheet", "Summary Worksheet Accurately Completed"),
                 ("ht_feedback_literacy", "Head Teacher Feedback - Literacy Assessment"),
                 ("submitted_gala", "Submitted GALA results"),
                 ("talking_wall", "Talking Wall on Display and update")
                ],
                header= True
               )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(SchoolMonitoringDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Pre-populate district admin field with the logged in user
        """
        if db_field.name == 'created_by_da':
            kwargs['queryset'] = DistrictAdminUser.objects.all()
            if len(DistrictAdminUser.objects.filter(user=request.user)) == 1:
                kwargs['initial'] = DistrictAdminUser.objects.get(user=request.user)
            return db_field.formfield(**kwargs)
        return super(SchoolMonitoringDataAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Pre-populate district admin field with the logged in user
        """
        if db_field.name == 'created_by_da':
            kwargs['queryset'] = DistrictAdminUser.objects.all()
            if len(DistrictAdminUser.objects.filter(user=request.user)) == 1:
                kwargs['initial'] = DistrictAdminUser.objects.get(user=request.user)
            return db_field.formfield(**kwargs)
        return super(TeacherPerformanceDataAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class LearnerPerformanceDataAdmin(ManagePermissions):
    list_display = ["emis", "gender", "total_number_pupils", "phonetic_awareness", "vocabulary",
                    "reading_comprehension", "writing_diction", "below_minimum_results", "minimum_results",
                    "desirable_results", "outstanding_results", "created_by", "created_at"]
    search_fields = ["emis__emis", "emis__name"]
    raw_id_fields = ("created_by",)
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Pre-populate district admin field with the logged in user
        """
        if db_field.name == 'created_by_da':
            kwargs['queryset'] = DistrictAdminUser.objects.all()
            if len(DistrictAdminUser.objects.filter(user=request.user)) == 1:
                kwargs['initial'] = DistrictAdminUser.objects.get(user=request.user)
            return db_field.formfield(**kwargs)
        return super(LearnerPerformanceDataAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


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
admin.site.register(DistrictAdminUser, DistrictAdminUserAdmin)
admin.site.register(SchoolMonitoringData, SchoolMonitoringDataAdmin)
admin.site.register(TeacherPerformanceData, TeacherPerformanceDataAdmin)
admin.site.register(LearnerPerformanceData, LearnerPerformanceDataAdmin)
admin.site.register(AcademicAchievementCode, AcademicAchievementCodeAdmin)

admin.site.register(SchoolDataDuplicateStore, SchoolDataDuplicateStoreAdmin)
admin.site.register(HeadTeacherDuplicateStore, HeadTeacherDuplicateStoreAdmin)
