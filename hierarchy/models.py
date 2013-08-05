from django.db import models


class Provinces(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of Province')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Province"


class Districts(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of District')
    province_id = models.ForeignKey('MonitorAndLearningQuizId',
                                    related_name='province_id ')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Monitor and Learning Quiz Question"



class Zones(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of Zone')
    district_id = models.ForeignKey('MonitorAndLearningQuizId',
                                    related_name='district_id ')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Zone"


class Schools(models.Model):
    EMIS = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=u'Name of School')
    school_id = models.ForeignKey('MonitorAndLearningQuizId',
                                   related_name='school_id ')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "School"
