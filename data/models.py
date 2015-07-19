from django.db import models
from django.contrib.auth.models import User
import mockups
from mockups.generators import ChoiceGenerator, IntegerGenerator
from tasks import vumi_fire_metric


class DistrictAdminUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name=u'First Name')
    last_name = models.CharField(max_length=50, verbose_name=u'Last Name')
    district = models.ForeignKey("hierarchy.District")
    id_number = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "District Admin"


class HeadTeacher(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=u'First Name')
    last_name = models.CharField(max_length=50, verbose_name=u'Last Name')
    gender = models.CharField(max_length=6, verbose_name=u'Gender')
    msisdn = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    is_zonal_head = models.BooleanField()
    zonal_head_name = models.CharField(max_length=100, verbose_name=u'Zonal Head')
    created_at = models.DateTimeField(auto_now_add=True)
    emis = models.ForeignKey('hierarchy.School',
                             null=True,
                             blank=True,
                             verbose_name=u'EMIS')

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Head Teacher"


class SchoolData(models.Model):
    emis = models.ForeignKey('hierarchy.School',
                             verbose_name=u'EMIS')
    name = models.CharField(max_length=100, verbose_name=u'Name')
    classrooms = models.IntegerField()
    teachers = models.IntegerField()
    boys = models.IntegerField(null=True)  # null = True, to prevent migration and unittest issues
    girls = models.IntegerField(null=True)  # null = True, to prevent migration and unittest issues
    teachers_g1 = models.IntegerField()
    teachers_g2 = models.IntegerField()
    boys_g2 = models.IntegerField()
    girls_g2 = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(HeadTeacher,
                                    verbose_name=u'Head Teacher')

    def __unicode__(self):
        return "%s" % self.emis

    class Meta:
        verbose_name_plural = "School Data"


# ####################################################################
    # Models to store duplicate migrations once deleted
# ####################################################################
class HeadTeacherDuplicateStore(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=u'First Name')
    last_name = models.CharField(max_length=50, verbose_name=u'Last Name')
    gender = models.CharField(max_length=6, verbose_name=u'Gender')
    msisdn = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    is_zonal_head = models.BooleanField()
    zonal_head_name = models.CharField(max_length=100, verbose_name=u'Zonal Head')
    created_at = models.DateTimeField(auto_now_add=True)
    emis = models.ForeignKey('hierarchy.School',
                             null=True,
                             blank=True,
                             verbose_name=u'EMIS')
    origin_id = models.IntegerField()

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Head Teacher Duplicate Store"


class SchoolDataDuplicateStore(models.Model):
    emis = models.ForeignKey('hierarchy.School',
                             verbose_name=u'EMIS')
    name = models.CharField(max_length=100, verbose_name=u'Name')
    classrooms = models.IntegerField()
    teachers = models.IntegerField()
    teachers_g1 = models.IntegerField()
    teachers_g2 = models.IntegerField()
    boys_g2 = models.IntegerField()
    girls_g2 = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(HeadTeacherDuplicateStore,
                                    verbose_name=u'Head Teacher Duplicate Store')
    origin_id = models.IntegerField()

    def __unicode__(self):
        return "%s" % self.emis

    class Meta:
        verbose_name_plural = "School Data Duplicate Store"

# ########################## End of Duplicate Data Storage ##########

class AcademicAchievementCode(models.Model):
    achievement = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s" % self.achievement

    class Meta:
        verbose_name = "Academic Achievment Code"


class SchoolMonitoringData(models.Model):
    YES_PROGRESS_NO_CHOICES = (
        ('yes', 'YES - completed'),
        ('yes_in_progress', 'YES - in progress'),
        ('no', 'NO')
    )
    YES_NO_CHOICES = (
        ('yes', 'YES'),
        ('no', 'NO')
    )
    SUBMITTED_CHOICES = (
        ('yes_cellphone', 'YES submitted by cell phone'),
        ('yes_paper', 'YES submitted paper form to DEBS office'),
        ('no', 'NO')
    )
    YES_UPDATED_NO_CHOICES = (
        ('yes', 'YES'),
        ('yes_not_updated', 'YES but not updated'),
        ('no', 'NO')
    )

    see_lpip = models.CharField(
        max_length=17, choices=YES_PROGRESS_NO_CHOICES,
        verbose_name=u'Saw School Learner Performance Improvement Plan')
    teaching = models.CharField(
        max_length=17, choices=YES_PROGRESS_NO_CHOICES,
        verbose_name=u'Activity for Improving Teaching',
        null=True, blank=True)
    learner_assessment = models.CharField(
        max_length=17, choices=YES_PROGRESS_NO_CHOICES,
        verbose_name=u'Activity for Improving Learner Assessment',
        null=True, blank=True)
    learning_materials = models.CharField(
        max_length=17, choices=YES_PROGRESS_NO_CHOICES,
        verbose_name=u'Activity for Acquiring Learning Materials',
        null=True, blank=True)
    learner_attendance = models.CharField(
        max_length=17, choices=YES_PROGRESS_NO_CHOICES,
        verbose_name=u'Activity for Improving Learner Attendance',
        null=True, blank=True)
    reading_time = models.CharField(
        max_length=17, choices=YES_PROGRESS_NO_CHOICES,
        verbose_name=u'Activity for Improving Reading Time',
        null=True, blank=True)
    struggling_learners = models.CharField(
        max_length=17, choices=YES_PROGRESS_NO_CHOICES,
        verbose_name=u'Extra Support for Struggling Learners',
        null=True, blank=True)
    g2_observation_results = models.CharField(
        max_length=17, choices=YES_PROGRESS_NO_CHOICES,
        verbose_name=u'Saw Grade 2 Reading Lesson Observation Results')
    ht_feedback = models.CharField(
        max_length=3, choices=YES_NO_CHOICES,
        verbose_name=u'Head Teacher Feedback',
        null=True, blank=True)
    submitted_classroom = models.CharField(
        max_length=39, choices=SUBMITTED_CHOICES,
        verbose_name=u'Submitted Classroom Observation Results',
        null=True, blank=True)
    gala_sheets = models.CharField(
        max_length=17, choices=YES_PROGRESS_NO_CHOICES,
        verbose_name=u'Saw GALA stimulus sheets')
    summary_worksheet = models.CharField(
        max_length=3, choices=YES_NO_CHOICES,
        verbose_name=u'Summary Worksheet Accurately Completed',
        null=True, blank=True)
    ht_feedback_literacy = models.CharField(
        max_length=3, choices=YES_NO_CHOICES,
        verbose_name=u'Head Teacher Feedback - Literacy Assessment',
        null=True, blank=True)
    submitted_gala = models.CharField(
        max_length=39, choices=SUBMITTED_CHOICES,
        verbose_name=u'Submitted GALA results',
        null=True, blank=True)
    talking_wall = models.CharField(
        max_length=19, choices=YES_UPDATED_NO_CHOICES,
        verbose_name=u'Talking Wall on Display and updated',
        null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    emis = models.ForeignKey('hierarchy.School',
                             verbose_name=u'EMIS')
    created_by = models.ForeignKey(HeadTeacher,
                                   verbose_name=u'Head Teacher',
                                   null=True,
                                   blank=True)
    created_by_da = models.ForeignKey(DistrictAdminUser,
                                      verbose_name=u'District Admin User',
                                      null=True,
                                      blank=True)
    def __unicode__(self):
        return "%s" % self.emis

    class Meta:
        verbose_name_plural = "School Monitoring Data"


class TeacherPerformanceData(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    EXPERIENCE_CHOICES = (
        ("0-3", '0 - 3 years'),
        ("4-8", '4 - 8 years'),
        ("9-12", "9 - 12 years"),
        ("13+", "13 years or more")
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                                verbose_name=u'Gender')
    age = models.IntegerField()
    years_experience = models.CharField(max_length=5,
                                        choices=EXPERIENCE_CHOICES)
    g2_pupils_present = models.IntegerField()
    g2_pupils_registered = models.IntegerField()
    classroom_environment_score = models.IntegerField()
    t_l_materials = models.IntegerField()
    pupils_materials_score = models.IntegerField()
    pupils_books_number = models.IntegerField()
    reading_lesson = models.IntegerField()
    pupil_engagement_score = models.IntegerField()
    attitudes_and_beliefs = models.IntegerField()
    training_subtotal = models.IntegerField()
    ts_number = models.IntegerField()
    reading_assessment = models.IntegerField(null=True) # null = True for new fields
    reading_total = models.IntegerField(null=True)  # Default is None for new fields
    created_at = models.DateTimeField(auto_now_add=True)
    academic_level = models.ForeignKey(AcademicAchievementCode,
                                    verbose_name=u'Academic Achievement')
    emis = models.ForeignKey('hierarchy.School',
                             verbose_name=u'EMIS')
    created_by = models.ForeignKey(HeadTeacher,
                                   verbose_name=u'Head Teacher',
                                   null=True,
                                   blank=True)
    created_by_da = models.ForeignKey(DistrictAdminUser,
                                      verbose_name=u'District Admin User',
                                      null=True,
                                      blank=True)
    def __unicode__(self):
        return "%s" % self.emis

    class Meta:
        verbose_name_plural = "Teacher Performance Data"


class LearnerPerformanceData(models.Model):
    GENDER_CHOICES = (
        ('boys', 'Boys'),
        ('girls', 'Girls')
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                                verbose_name=u'Gender')
    total_number_pupils = models.IntegerField()
    phonetic_awareness = models.IntegerField()
    vocabulary = models.IntegerField()
    reading_comprehension = models.IntegerField()
    writing_diction = models.IntegerField()
    below_minimum_results = models.IntegerField()
    minimum_results = models.IntegerField()
    desirable_results = models.IntegerField()
    outstanding_results = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    emis = models.ForeignKey('hierarchy.School',
                             verbose_name=u'EMIS')
    created_by = models.ForeignKey(HeadTeacher,
                                   null=True,
                                   blank=True,
                                   verbose_name=u'Head Teacher')
    created_by_da = models.ForeignKey(DistrictAdminUser,
                                      verbose_name=u'District Admin User',
                                      null=True,
                                      blank=True)
    def __unicode__(self):
        return "%s" % self.emis

    class Meta:
        verbose_name_plural = "Learner Performance Data"


class InboundSMS(models.Model):
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(HeadTeacher,
                                    verbose_name=u'Header Teacher')

    def __unicode__(self):
        return "%s" % self.message

    class Meta:
        verbose_name = "Inbound SMS"


# custom mockups for data generation

class GenderGenerator(ChoiceGenerator):
    choices = [u"male", u"female"]


class TeacherPerformanceDataFactory(mockups.Factory):
    gender = GenderGenerator()
    age = IntegerGenerator(min_value=29, max_value=50)
    years_experience = IntegerGenerator(min_value=1, max_value=30)
    g2_pupils_present = IntegerGenerator(min_value=30, max_value=50)
    g2_pupils_registered = IntegerGenerator(min_value=30, max_value=50)
    classroom_environment_score = IntegerGenerator(min_value=1, max_value=10)
    t_l_materials = IntegerGenerator(min_value=1, max_value=10)
    pupils_materials_score = IntegerGenerator(min_value=1, max_value=10)
    pupils_books_number = IntegerGenerator(min_value=0, max_value=20)
    reading_lesson = IntegerGenerator(min_value=1, max_value=10)
    pupil_engagement_score = IntegerGenerator(min_value=1, max_value=10)
    attitudes_and_beliefs = IntegerGenerator(min_value=1, max_value=10)
    training_subtotal = IntegerGenerator(min_value=1, max_value=10)
    ts_number = IntegerGenerator(min_value=10000, max_value=99999)


class TeacherPerformanceDataMockup(mockups.Mockup):
    factory = TeacherPerformanceDataFactory


mockups.register(TeacherPerformanceData, TeacherPerformanceDataMockup)


class LearnerPerformanceDataFactory(mockups.Factory):
    gender = GenderGenerator()
    total_number_pupils = IntegerGenerator(min_value=1, max_value=30)
    phonetic_awareness = IntegerGenerator(min_value=1, max_value=10)
    vocabulary = IntegerGenerator(min_value=1, max_value=10)
    reading_comprehension = IntegerGenerator(min_value=1, max_value=10)
    writing_diction = IntegerGenerator(min_value=1, max_value=10)
    below_minimum_results = IntegerGenerator(min_value=1, max_value=30)
    minimum_results = IntegerGenerator(min_value=1, max_value=10)
    desirable_results = IntegerGenerator(min_value=1, max_value=10)
    outstanding_results = IntegerGenerator(min_value=1, max_value=10)


class LearnerPerformanceDataMockup(mockups.Mockup):
    factory = LearnerPerformanceDataFactory


mockups.register(LearnerPerformanceData, LearnerPerformanceDataMockup)

# Make sure new entries are sent to Vumi Metric via Celery
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=HeadTeacher)
def fire_ht_metric_if_new(sender, instance, created, **kwargs):
    if created:
        vumi_fire_metric.delay(metric="sum.head_teachers_registrations.total", value=1, agg="sum")

@receiver(post_save, sender=LearnerPerformanceData)
def fire_lp_metric_if_new(sender, instance, created, **kwargs):
    if created:
        vumi_fire_metric.delay(metric="sum.learner_performanace_reports.total", value=1, agg="sum")

@receiver(post_save, sender=TeacherPerformanceData)
def fire_tp_metric_if_new(sender, instance, created, **kwargs):
    if created:
        vumi_fire_metric.delay(metric="sum.teacher_performanace_reports.total", value=1, agg="sum")

@receiver(post_save, sender=SchoolMonitoringData)
def fire_sm_metric_if_new(sender, instance, created, **kwargs):
    if created:
        vumi_fire_metric.delay(metric="sum.school_monitoring_reports.total", value=1, agg="sum")

