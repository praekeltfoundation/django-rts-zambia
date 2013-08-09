from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from models import (HeadTeacher)
from hierarchy.api import SchoolResource
from tastypie.utils import dict_strip_unicode_keys
from tastypie import http


class HeadTeacherResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    emis_id = fields.ForeignKey(SchoolResource, 'emis_id', full=True)
    
    class Meta:
        queryset = HeadTeacher.objects.all()
        resource_name = "data/headteacher"
        list_allowed_methods = ['post', 'get', 'put'] 
        authorization = Authorization()
        include_resource_uri = False

    # def post_list(self, request, **kwargs):
    #     """
    #     Creates a new resource/object with the provided data.

    #     Calls ``obj_create`` with the provided data and returns a response
    #     with the new resource's location.

    #     If a new resource is created, return ``HttpCreated`` (201 Created).
    #     If ``Meta.always_return_data = True``, there will be a populated body
    #     of serialized data.
    #     """
    #     deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
    #     deserialized = self.alter_deserialized_detail_data(request, deserialized)
    #     # bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
    #     # updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
    #     # location = self.get_resource_uri(updated_bundle)

    #     # if not self._meta.always_return_data:
    #     #     return http.HttpCreated(location=location)
    #     # else:
    #     #     updated_bundle = self.full_dehydrate(updated_bundle)
    #     #     updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
    #     #     return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)
