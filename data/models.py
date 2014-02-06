from django.db import models
import mockups
from mockups.generators import ChoiceGenerator, IntegerGenerator


class DistrictAdminUser(models.Model):
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


class TeacherPerformanceData(models.Model):
    gender = models.CharField(max_length=6, verbose_name=u'Gender')
    age = models.IntegerField()
    years_experience = models.CharField(max_length=5)
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
                                   null=True)
    created_by_da = models.ForeignKey(DistrictAdminUser,
                                      verbose_name=u'District Admin User',
                                      null=True)
    def __unicode__(self):
        return "%s" % self.emis

    class Meta:
        verbose_name_plural = "Teacher Performance Data"


class LearnerPerformanceData(models.Model):
    gender = models.CharField(max_length=6, verbose_name=u'Gender')
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
                                   verbose_name=u'Head Teacher')
    created_by_da = models.ForeignKey(DistrictAdminUser,
                                      verbose_name=u'District Admin User',
                                      null=True)
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
