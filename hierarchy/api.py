from tastypie.resources import ModelResource
from tastypie import fields
from models import (Province, District, Zone, School)


class ProvinceResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    class Meta:
        resource_name = "hierarchy"
        allowed_methods = ['get']
        include_resource_uri = False
        queryset = Province.objects.all()


class DistrictResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    path = 'hierarchy.api.ProvinceResource'
    province_id = fields.ForeignKey(path, 'province_id', full=True)
    class Meta:
        resource_name = "hierarchy"
        allowed_methods = ['get']
        include_resource_uri = False
        queryset = District.objects.all()


class ZoneResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    path = 'hierarchy.api.DistrictResource'
    district_id = fields.ForeignKey(path, 'district_id', full=True)
    class Meta:
        resource_name = "hierarchy"
        allowed_methods = ['get']
        include_resource_uri = False
        queryset = Zone.objects.all()


class SchoolResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    path = 'hierarchy.api.ZoneResource'
    zone_id = fields.ForeignKey(ZoneResource, 'zone_id', full=True)
    class Meta:
        resource_name = "hierarchy"
        allowed_methods = ['get']
        include_resource_uri = False
        queryset = School.objects.all()
