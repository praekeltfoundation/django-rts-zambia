from django.db import models
from django.contrib.auth.models import User


class UserDistrict(models.Model):
    user = models.OneToOneField(User)
    district = models.ForeignKey('hierarchy.District')
