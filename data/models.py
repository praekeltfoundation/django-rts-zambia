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
    gender = models.CharField(max_length=6, verbose_name=u'Gender')
    age = models.IntegerField()
    years_experience = models.IntegerField()
    g2_pupils_present = models.IntegerField()
    g2_pupils_registered = models.IntegerField()
    classroom_environment_score = models.IntegerField()
    t_l_materials = models.IntegerField()
    pupils_materials_score = models.IntegerField()
    pupils_books_number = models.IntegerField()
    reading_lesson = models.IntegerField()
    pupil_engagment_score = models.IntegerField()
    attitudes_and_beliefs = models.IntegerField()
    training_subtotal = models.IntegerField()
    local_reading_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    academic_level = models.IntegerField()  # Used IntField for now
    emis = models.ForeignKey('hierarchy.School',
                             verbose_name=u'EMIS Number')
    created_by = models.ForeignKey(HeadTeacher,
                                   verbose_name=u'Teacher')



class LearnerPerfomanceData(models.Model):
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
                             verbose_name=u'EMIS Number')
    created_by = models.ForeignKey(HeadTeacher,
                                   verbose_name=u'Teacher')
