from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of Province')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "1. Province"


class District(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of District')
    province = models.ForeignKey('Province',
                                  verbose_name=u'Province')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "2. District"



class Zone(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name of Zone')
    district = models.ForeignKey('District',
                                 verbose_name=u'District')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "3. Zone"


class School(models.Model):
    emis = models.IntegerField(unique=True, max_length=8)
    name = models.CharField(max_length=50, verbose_name=u'Name of School')
    zone = models.ForeignKey('Zone',
                             verbose_name=u'Zone')

    def __unicode__(self):
        return "%s" % self.emis

    class Meta:
        verbose_name = "4. School"
