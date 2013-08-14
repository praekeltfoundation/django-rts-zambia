from django.db import models


class HeadTeacher(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=u'First Name')
    last_name = models.CharField(max_length=50, verbose_name=u'Last Name')
    gender = models.CharField(max_length=6, verbose_name=u'Gender')
    msisdn = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    is_zonal_head = models.BooleanField()
    zonal_head_name = models.CharField(max_length=100, verbose_name=u'Zonal Head Name')
    created_at = models.DateTimeField(auto_now_add=True)
    emis = models.ForeignKey('hierarchy.School',
                             null=True,
                             blank=True,
                             verbose_name=u'EMIS Number')

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Head Teacher"


class SchoolData(models.Model):
    emis = models.ForeignKey('hierarchy.School',
                             verbose_name=u'EMIS Number')
    name = models.CharField(max_length=100, verbose_name=u'Name of School')
    classrooms = models.IntegerField()
    teachers = models.IntegerField()
    teachers_g1 = models.IntegerField()
    teachers_g2 = models.IntegerField()
    boys_g2 = models.IntegerField()
    girls_g2 = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(HeadTeacher,
                                    verbose_name=u'Teacher')

    def __unicode__(self):
        return "%s" % self.emis

    class Meta:
        verbose_name = "School Data"


class TeacherPerfomanceData(models.Model):
    gender = models.CharField(max_length=6, null=True, blank=True, verbose_name=u'Gender')
    age = models.IntegerField(null=True, blank=True)
    years_experience = models.IntegerField(null=True, blank=True)
    g2_pupils_present = models.IntegerField(null=True, blank=True)
    g2_pupils_registered = models.IntegerField(null=True, blank=True)
    classroom_environment_score = models.IntegerField()
    t_l_materials = models.IntegerField(null=True, blank=True)
    pupils_materials_score = models.IntegerField(null=True, blank=True)
    pupils_books_number = models.IntegerField(null=True, blank=True)
    reading_lesson = models.IntegerField(null=True, blank=True)
    pupil_engagment_score = models.IntegerField(null=True, blank=True)
    attitudes_and_beliefs = models.IntegerField(null=True, blank=True)
    training_subtotal = models.IntegerField(null=True, blank=True)
    local_reading_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    academic_level = models.IntegerField(null=True, blank=True)  # Used IntField for now
    emis = models.ForeignKey('hierarchy.School',
                             verbose_name=u'EMIS Number')
    created_by = models.ForeignKey(HeadTeacher,
                                   verbose_name=u'Teacher')



class LearnerPerfomanceData(models.Model):
    gender = models.CharField(max_length=6, null=True, blank=True, verbose_name=u'Gender')
    total_number_pupils = models.IntegerField(null=True, blank=True)
    phonetic_awareness = models.IntegerField(null=True, blank=True)
    vocabulary = models.IntegerField(null=True, blank=True)
    reading_comprehension = models.IntegerField(null=True, blank=True)
    writing_diction = models.IntegerField(null=True, blank=True)
    below_minimum_results = models.IntegerField(null=True, blank=True)
    minimum_results = models.IntegerField(null=True, blank=True)
    desirable_results = models.IntegerField(null=True, blank=True)
    outstanding_results = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    emis = models.ForeignKey('hierarchy.School',
                             verbose_name=u'EMIS Number')
    created_by = models.ForeignKey(HeadTeacher,
                                   verbose_name=u'Teacher')
