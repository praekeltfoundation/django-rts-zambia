from tastypie.resources import ModelResource
from tastypie import fields
from models import (HeadTeacher)


class HeadTeacherResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    class Meta:
        resource_name = "data/headteacher"
        allowed_methods = ['get']
        include_resource_uri = False
        queryset = HeadTeacher.objects.all()

