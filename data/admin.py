from django.contrib import admin
from models import (SchoolData, HeadTeacher, InboundSMS, AcademicAchievementCode,
                    TeacherPerformanceData, LearnerPerformanceData)
from actions import export_select_fields_csv_action
from rts.utils import DistrictIdFilter



class SchoolDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "name", "classrooms", "teachers",
                    "teachers_g1", "teachers_g2", "boys_g2", "girls_g2", "created_by", "created_at"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
               fields= [
                ("emis", "Emis"),
                ("name", "Name"),
                ("classrooms", "Classrooms"),
                ("teachers", "Teachers"),
                ("teachers_g1", "Grade 1 Teachers"),
                ("teachers_g2", "Grade 2 Teachers"),
                ("boys_g2", "Grade 2 Boys"),
                ("girls_g2", "Grade 2 Girls"),
                ("created_by", "Created By"),
                ("created_at", "Created At"),
               ],
               header=True
              )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(SchoolDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


class HeadTeacherAdmin(admin.ModelAdmin):
    list_display = ["emis", "first_name", "last_name", "msisdn", "gender", "date_of_birth", "is_zonal_head", "zonal_head_name","created_at"]
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


class TeacherPerformanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "gender", "age", "years_experience", "g2_pupils_present", "g2_pupils_registered",
                    "classroom_environment_score", "t_l_materials", "pupils_materials_score",
                    "pupils_books_number", "reading_lesson", "pupil_engagement_score", "attitudes_and_beliefs",
                    "training_subtotal", "ts_number", "academic_level", "created_by", "created_at"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
               fields= [
                ("emis", "Emis"),
                ("gender", "Gender"),
                ("age", "Age"),
                ("years_experience", "Years of Experience"),
                ("g2_pupils_present", "Grade 2 Pupils Present"),
                ("g2_pupils_registered", "Grade 2 Pupils Registered"),
                ("classroom_environment_score", "Classroom Environment Score"),
                ("t_l_materials", "T L Materials"),
                ("pupils_materials_score", "Pupils Materials Score"),
                ("pupils_books_number", "Pupils Book Number"),
                ("reading_lesson", "Reading lesson"),
                ("pupil_engagement_score", "Pupil Engagement Score"),
                ("attitudes_and_beliefs", "Attitudes And Beliefs"),
                ("training_subtotal", "Training Subtotal"),
                ("ts_number", "TS Number"),
                ("academic_level", "Academic Level"),
                ("created_by", "Created By"),
                ("created_at", "Created At"),
               ],
               header=True
              )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(TeacherPerformanceDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


class LearnerPerformanceDataAdmin(admin.ModelAdmin):
    list_display = ["emis", "gender", "total_number_pupils", "phonetic_awareness", "vocabulary",
                    "reading_comprehension", "writing_diction", "below_minimum_results", "minimum_results",
                    "desirable_results", "outstanding_results", "created_by", "created_at"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
               fields= [
                ("emis", "Emis"),
                ("gender", "Gender"),
                ("total_number_pupils", "Total Number of Pupils"),
                ("phonetic_awareness", "Phonetic Awareness"),
                ("vocabulary", "Vocabulary"),
                ("reading_comprehension", "Reading Comprehension"),
                ("writing_diction", "Writing Diction"),
                ("below_minimum_results", "Below Minimum Results"),
                ("minimum_results", "Minimum Results"),
                ("desirable_results", "Desirable Results"),
                ("outstanding_results", "Outstanding Results"),
                ("created_by", "Created By"),
                ("created_at", "Created At"),
               ],
               header=True
              )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(LearnerPerformanceDataAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


class InboundSMSAdmin(admin.ModelAdmin):
    list_display = ["message", "created_by", "created_at"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file",
               fields= [
                ("message", "Message"),
                ("created_by", "Created By"),
                ("created_at", "Created At"),
               ],
               header=True
              )]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(InboundSMSAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


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
