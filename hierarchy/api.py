# Django
from django.conf.urls import url

# Project
from models import (Province, District, Zone, School)
from rts.utils import (CSVSerializer, CSVModelResource,
                       OverrideApiAuthentication)

# Third Party
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS, ALL


# Normal JSON serializer
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
            url(r"^(?P<resource_name>%s)/emis/(?P<emis>[\w\d_.-]+)/$" %
                self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]


class EmisResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    class Meta:
        resource_name = "hierarchy"
        allowed_methods = ['get']
        max_limit = None
        include_resource_uri = False
        queryset = School.objects.all()
        fields = ['emis']
        filtering = {
            'emis': ALL}


# CSV serializer
class ProvinceResourceCSVDownload(CSVModelResource):
    """
    Returns csv instead of json
    GET Province CSV
    ::

    "url": "<base_url>/api/v1/csv/province/?username=name&api_key=key,
    "method": "GET",
    """
    class Meta:
        resource_name = "csv/province"
        allowed_methods = ['get']
        include_resource_uri = False
        queryset = Province.objects.all()
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()


class DistrictResourceCSVDownload(CSVModelResource):
    """
    Returns csv instead of json
    GET District CSV
    ::

    "url": "<base_url>/api/v1/csv/district/?username=name&api_key=key,
    "method": "GET",
    """
    class Meta:
        resource_name = "csv/district"
        allowed_methods = ['get']
        include_resource_uri = False
        queryset = District.objects.all()
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()

    def dehydrate(self, bundle):
        bundle.data['province'] = bundle.obj.province.id
        return bundle


class ZoneResourceCSVDownload(CSVModelResource):
    """
    Returns csv instead of json
    GET Zone CSV
    ::

    "url": "<base_url>/api/v1/csv/zone/?username=name&api_key=key,
    "method": "GET",
    """
    class Meta:
        resource_name = "csv/zone"
        allowed_methods = ['get']
        include_resource_uri = False
        queryset = Zone.objects.all()
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()

    def dehydrate(self, bundle):
        bundle.data['district'] = bundle.obj.district.id
        return bundle


class SchoolResourceCSVDownload(CSVModelResource):
    """
    Returns csv instead of json
    GET School CSV
    ::

    "url": "<base_url>/api/v1/csv/school/?username=name&api_key=key,
    "method": "GET",
    """
    zone = fields.ForeignKey(ZoneResource, 'zone')

    class Meta:
        max_limit = None
        resource_name = "csv/school"
        allowed_methods = ['get']
        include_resource_uri = False
        queryset = School.objects.all()
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()

    def dehydrate(self, bundle):
        bundle.data['zone'] = bundle.obj.zone.id
        return bundle


class EmisResourceCSVDownload(CSVModelResource):
    """
    Returns csv instead of json
    """
    class Meta:
        resource_name = "csv/hierarchy"
        allowed_methods = ['get']
        max_limit = None
        include_resource_uri = False
        queryset = School.objects.all()
        fields = ['emis']
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()
