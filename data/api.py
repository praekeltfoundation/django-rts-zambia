from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie import fields
from models import (HeadTeacher, SchoolData)


class HeadTeacherResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis', full=True)

    class Meta:
        queryset = HeadTeacher.objects.all()
        resource_name = "data/headteacher"
        list_allowed_methods = ['post', 'get'] 
        authorization = Authorization()
        include_resource_uri = False
        always_return_data = True
        filtering = {
            'emis': ALL_WITH_RELATIONS}


class SchoolDataResource(ModelResource):
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis', full=True)
    created_by = fields.ForeignKey(HeadTeacherResource, 'created_by', full=True)

    class Meta:
        queryset = SchoolData.objects.all()
        resource_name = "data/schooldata"
        list_allowed_methods = ['post', 'get'] 
        authorization = Authorization()
        include_resource_uri = False
        filtering = {
            'emis': ALL_WITH_RELATIONS}