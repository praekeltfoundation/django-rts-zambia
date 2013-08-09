from django.db import models
from hierarchy.models import School


class HeadTeacher(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=u'First Name')
    last_name = models.CharField(max_length=50, verbose_name=u'Last Name')
    gender = models.CharField(max_length=6, verbose_name=u'Gender')
    msisdn = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    is_zonal_head = models.BooleanField()
    emis_id = models.ForeignKey('hierarchy.School',
                                null=True,
                                blank=True,
                                verbose_name=u'EMIS Number')
    created_at = models.DateField()

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Head Teacher"


class SchoolData(models.Model):
    emis_id = models.ForeignKey('hierarchy.School',
                                verbose_name=u'EMIS Number')
    classrooms = models.IntegerField()
    teachers = models.IntegerField()
    teachers_g1 = models.IntegerField()
    teachers_g2 = models.IntegerField()
    boys_g2 = models.IntegerField()
    girls_g2 = models.IntegerField()
    created_at = models.DateField()
    created_by = models.ForeignKey(HeadTeacher,
                                    verbose_name=u'EMIS Number')

    def __unicode__(self):
        return "%s" % self.emis_id

    class Meta:
        verbose_name = "School Data"
