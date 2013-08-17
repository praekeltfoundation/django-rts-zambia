from tastypie.resources import ModelResource
from tastypie import fields
from models import (Province, District, Zone, School)
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from django.conf.urls import url


class ProvinceResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    class Meta:
        resource_name = "province"
        allowed_methods = ['get']
        include_resource_uri = True
        queryset = Province.objects.all()


class DistrictResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    province = fields.ForeignKey(ProvinceResource, 'province', full=True)
    class Meta:
        resource_name = "district"
        allowed_methods = ['get']
        include_resource_uri = True
        queryset = District.objects.all()


class ZoneResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    district = fields.ForeignKey(DistrictResource, 'district', full=True)
    class Meta:
        resource_name = "zone"
        allowed_methods = ['get']
        include_resource_uri = True
        queryset = Zone.objects.all()


class SchoolResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    zone = fields.ForeignKey(ZoneResource, 'zone', full=True)
    class Meta:
        resource_name = "school"
        allowed_methods = ['get']
        include_resource_uri = True
        queryset = School.objects.all()
        filtering = {
            'emis': ALL_WITH_RELATIONS}

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/emis/(?P<emis>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]


class EmisResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    # zone = fields.ForeignKey(ZoneResource, 'zone', full=True)
    class Meta:
        resource_name = "hierarchy"
        allowed_methods = ['get']
        limit = 0
        include_resource_uri = False
        queryset = School.objects.all()
        fields = ['emis']
        filtering = {
            'emis': ALL}

