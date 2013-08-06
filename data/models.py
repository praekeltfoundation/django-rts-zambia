from django.db import models
from hierarchy.models import School


class SchoolData(models.Model):
    EMIS = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=u'Name of School')
    zone_id = models.ForeignKey('Zones',
                                   related_name='zone_id ')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "School"


class HeadTeacher(models.Model):
    name_first = models.CharField(max_length=50, verbose_name=u'First Name')
    name_last = models.CharField(max_length=50, verbose_name=u'Last Name')
    gender = models.CharField(max_length=2, verbose_name=u'Gender',
                              choices =(("M", "Male"), ("F", "Female")))
    date_of_birth = models.DateField()
    is_zonal_head = models.BooleanField()
    EMIS_id = models.IntegerField(School,
                                  related_name="EMIS")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Province"
