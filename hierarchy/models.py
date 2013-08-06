from django.db import models


class Provinces(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of Province')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Province"


class Districts(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of District')
    province_id = models.ForeignKey('Provinces',
                                    related_name='province_id ')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "District"



class Zones(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of Zone')
    district_id = models.ForeignKey('Districts',
                                    related_name='district_id ')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Zone"


class Schools(models.Model):
    EMIS = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=u'Name of School')
    zone_id = models.ForeignKey('Zones',
                                   related_name='zone_id ')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "School"
