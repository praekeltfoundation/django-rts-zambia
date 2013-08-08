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
        resource_name = "hierarchy"
        allowed_methods = ['get']
        include_resource_uri = False
        queryset = School.objects.all()
