from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of Province')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Province"


class District(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of District')
    province_id = models.ForeignKey('Province',
                                    related_name='province_id',
                                    verbose_name=u'Province')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "District"



class Zone(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of Zone')
    district_id = models.ForeignKey('District',
                                    related_name='district_id',
                                    verbose_name=u'District')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Zone"


class School(models.Model):
    EMIS = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=u'Name of School')
    zone_id = models.ForeignKey('Zone',
                                related_name='zone_id',
                                verbose_name=u'Zone')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "School"
