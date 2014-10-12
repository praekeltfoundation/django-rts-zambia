from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.paginator import Paginator
from models import (HeadTeacher, SchoolData, TeacherPerformanceData,
                    LearnerPerformanceData, SchoolMonitoringData, InboundSMS,
                    AcademicAchievementCode, DistrictAdminUser)
from django.conf.urls import url

# Project
from rts.utils import (CSVSerializer, CSVModelResource,
                       OverrideApiAuthentication)


class DistrictAdminUserResource(ModelResource):
    """
    GET District Admin
    ::

    "url": "<base_url>/api/v1/district_admin/,
    "method": "GET",

    POST FORMAT_MODULE_PATH
    ::

    "url": "<base_url>/api/v1/district_admin/,
    "method": "POST",
    "content_type": "application/json",
    "body": {"first_name": "test_first_name",
    "last_name": "test_last_name",
    "date_of_birth": "2012-10-12T10:00:00",
    "district": "/api/v1/district/1/",
    "id_number": "za123456789"}
    """
    district = fields.ForeignKey("hierarchy.api.DistrictResource", 'district', full=True)
    class Meta:
        queryset = DistrictAdminUser.objects.all()
        resource_name = "district_admin"
        list_allowed_methods = ['post', 'get']
        authorization = Authorization()
        include_resource_uri = True
        always_return_data = True
        paginator_class = Paginator

class HeadTeacherResource(ModelResource):
    """
    POSTING DATA
    {
    "url": "<base_url>/api/v1/data/headteacher/",,
    "method": "POST",
    "content_type": "application/json",
    "body": {
                "first_name": "abc",
                "last_name": "def",
                "created_at": "2012-10-12T10:00:00Z",
                "date_of_birth": "1962-10-12T10:00:00Z",
                "gender": "male",
                "msisdn": "0726961764",
                "emis": "/api/v1/school/emis/4811/"
            }

    GET SPECIFIC EMIS
    "url": "<base_url>/api/v1/data/headteacher/?emis__emis=4817",,
    "method": "GET",

    IS_ZONAL_HEAD
    "url": "<base_url>/api/v1/data/headteacher/?is_zonal_head=True",
    "method": "GET",
    # Filter can be [True, true, 1] for true and [False, false, 0] for false
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis', full=True)

    class Meta:
        queryset = HeadTeacher.objects.all()
        resource_name = "data/headteacher"
        list_allowed_methods = ['post', 'get', 'put']
        authorization = Authorization()
        include_resource_uri = True
        always_return_data = True
        filtering = {
            'emis': ALL_WITH_RELATIONS,
            'is_zonal_head': ALL}
        paginator_class = Paginator

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/emis/(?P<emis>[\w\d_.-]+)/$" %
                self._meta.resource_name, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]


class SchoolDataResource(ModelResource):
    """
    POSTING DATA

    "url": "<base_url>/api/v1/data/school/",
    "method": "POST",
    "content_type": "application/json",
    "body": {
                "name": "test_name",
                "classrooms": 30,
                "teachers": 40,
                "teachers_g1": 4,
                "teachers_g2": 8,
                "boys_g2": 15,
                "girls_g2": 12,
                "created_by": "/api/data/headteacher/emis/4813/",
                "emis": "/api/v1/school/emis/4813/"
            }
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis', full=True)
    created_by = fields.ForeignKey(HeadTeacherResource,
                                   'created_by', full=True)

    class Meta:
        queryset = SchoolData.objects.all()
        resource_name = "data/school"
        list_allowed_methods = ['post', 'get']
        authorization = Authorization()
        include_resource_uri = True
        always_return_data = True
        filtering = {
            'created_by': ALL_WITH_RELATIONS,
            'emis': ALL_WITH_RELATIONS}
        paginator_class = Paginator


class AcademicAchievementCodeResource(ModelResource):
    """
    GET SPECIFIC HEADTEACHER ON EMIS

    "url": "<base_url>/api/v1/data/achievement/<id>/,,
    "method": "GET",
    """
    class Meta:
        queryset = AcademicAchievementCode.objects.all()
        resource_name = "data/achievement"
        list_allowed_methods = ['get']
        authorization = Authorization()
        include_resource_uri = True
        always_return_data = True
        paginator_class = Paginator


class SchoolMonitoringDataResource(ModelResource):
    """
    POSTING DATA

    "url": "<base_url>/api/v1/data/school_monitoring/",
    "body": {
                "data": "data",
                "created_by": "/api/v1/data/headteacher/emis/4813/",
                "emis": "/api/v1/school/emis/4813/"
            }
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis', full=True)
    created_by = fields.ForeignKey(HeadTeacherResource,
                                   'created_by',
                                   null=True,
                                   full=True)
    created_by_da = fields.ForeignKey(DistrictAdminUserResource,
                                      'created_by_da',
                                       null=True,
                                       full=True)

    class Meta:
        queryset = SchoolMonitoringData.objects.all()
        resource_name = "data/school_monitoring"
        list_allowed_methods = ['post', 'get']
        authorization = Authorization()
        include_resource_uri = True
        always_return_data = True
        filtering = {
            'created_by': ALL_WITH_RELATIONS,
            'emis': ALL_WITH_RELATIONS}
        paginator_class = Paginator


class TeacherPerformanceDataResource(ModelResource):
    """
    POSTING DATA

    "url": "<base_url>/api/v1/data/teacherperformance/",
    "body": {
                "data": "data",
                "academic_level": "/api/data/achievement/8/",
                "created_by": "/api/data/headteacher/emis/4813/",
                "emis": "/api/v1/school/emis/4813/"
            }
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis', full=True)
    created_by = fields.ForeignKey(HeadTeacherResource,
                                   'created_by',
                                   null=True,
                                   full=True)
    created_by_da = fields.ForeignKey(DistrictAdminUserResource,
                                      'created_by_da',
                                       null=True,
                                       full=True)
    academic_level = fields.ForeignKey(AcademicAchievementCodeResource,
                                       'academic_level', full=True)

    class Meta:
        queryset = TeacherPerformanceData.objects.all()
        resource_name = "data/teacherperformance"
        list_allowed_methods = ['post', 'get']
        authorization = Authorization()
        include_resource_uri = True
        always_return_data = True
        filtering = {
            'created_by': ALL_WITH_RELATIONS,
            'emis': ALL_WITH_RELATIONS}
        paginator_class = Paginator


class LearnerPerformanceDataResource(ModelResource):
    """
    POSTING DATA

    "url": "<base_url>/api/v1/data/learnerperformance/",
    "body": {
                "data": "data",
                "created_by": "/api/v1/data/headteacher/emis/4813/",
                "emis": "/api/v1/school/emis/4813/"
            }
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis', full=True)
    created_by = fields.ForeignKey(HeadTeacherResource,
                                   'created_by',
                                   null=True,
                                   full=True)
    created_by_da = fields.ForeignKey(DistrictAdminUserResource,
                                      'created_by_da',
                                       null=True,
                                       full=True)

    class Meta:
        queryset = LearnerPerformanceData.objects.all()
        resource_name = "data/learnerperformance"
        list_allowed_methods = ['post', 'get']
        authorization = Authorization()
        include_resource_uri = True
        always_return_data = True
        filtering = {
            'created_by': ALL_WITH_RELATIONS,
            'emis': ALL_WITH_RELATIONS}
        paginator_class = Paginator


class InboundSMSResource(ModelResource):
    """
    GET SMS
    ::

    "url": "<base_url>/api/v1/data/sms/",,
    "method": "GET",

    POSTING DATA

    "url": "<base_url>/api/v1/data/sms/",
    "body": {
                "message": "test_name",
                "created_by": "/api/v1/data/sms/1/",
            }
    """
    created_by = fields.ForeignKey(HeadTeacherResource,
                                   'created_by', full=True)

    class Meta:
        queryset = InboundSMS.objects.all()
        resource_name = "data/sms"
        list_allowed_methods = ['post', 'get']
        authorization = Authorization()
        include_resource_uri = True
        always_return_data = True
        filtering = {
            'created_by': ALL_WITH_RELATIONS}
        paginator_class = Paginator


# =========================================================================
# This is the CSV download function
# =========================================================================
class HeadTeacherCSVDownloadResource(CSVModelResource):
    """
    GET Head Teacher CSV
    ::

    "url": "<base_url>/api/v1/csv/data/headteacher/?username=name&api_key=key,
    "method": "GET",
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis')

    class Meta:
        queryset = HeadTeacher.objects.all()
        resource_name = "csv/data/headteacher"
        list_allowed_methods = ['get']
        include_resource_uri = False
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()
        paginator_class = Paginator

    def dehydrate(self, bundle):
        bundle.data['emis'] = bundle.obj.emis.id
        return bundle


class SchoolDataCSVDownloadResource(CSVModelResource):
    """
    GET School Data CSV
    ::

    "url": "<base_url>/api/v1/csv/data/school/?username=name&api_key=key,
    "method": "GET",
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis')
    created_by = fields.ForeignKey(HeadTeacherResource, 'created_by')

    class Meta:
        queryset = SchoolData.objects.all()
        resource_name = "csv/data/school"
        list_allowed_methods = ['get']
        include_resource_uri = False
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()
        paginator_class = Paginator

    def dehydrate(self, bundle):
        bundle.data['emis'] = bundle.obj.emis.id
        bundle.data['created_by'] = bundle.obj.created_by.id
        return bundle


class AcademicAchievementCodeCSVDownloadResource(CSVModelResource):
    """
    GET Academic Achievement Code CSV
    ::

    "url": "<base_url>/api/v1/csv/data/achievement/?username=name&api_key=key,
    "method": "GET",
    """
    class Meta:
        queryset = AcademicAchievementCode.objects.all()
        resource_name = "csv/data/achievement"
        list_allowed_methods = ['get']
        authorization = Authorization()
        include_resource_uri = False
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()
        paginator_class = Paginator


class SchoolMonitoringDataCSVDownloadResource(CSVModelResource):
    """
    GET School Monitoring Data CSV
    ::

    "url": "<base_url>/api/v1/csv/data/school_monitoring/?username=name&api_key=key,
    "method": "GET",
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis')
    created_by = fields.ForeignKey(HeadTeacherResource, 'created_by')

    class Meta:
        queryset = SchoolMonitoringData.objects.all()
        resource_name = "csv/data/school_monitoring"
        list_allowed_methods = ['get']
        include_resource_uri = False
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()
        paginator_class = Paginator

    def dehydrate(self, bundle):
        bundle.data['emis'] = bundle.obj.emis.id
        bundle.data['created_by'] = bundle.obj.created_by.id
        return bundle


class TeacherPerformanceDataCSVDownloadResource(CSVModelResource):
    """
    GET Teacher Perfomance Data CSV
    ::

    "url": "<base_url>/api/v1/csv/data/teacherperformance/?username=name&api_key=key,
    "method": "GET",
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis')
    created_by = fields.ForeignKey(HeadTeacherResource, 'created_by')
    academic_level = fields.ForeignKey(AcademicAchievementCodeResource,
                                       'academic_level')

    class Meta:
        queryset = TeacherPerformanceData.objects.all()
        resource_name = "csv/data/teacherperformance"
        list_allowed_methods = ['get']
        include_resource_uri = False
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()
        paginator_class = Paginator

    def dehydrate(self, bundle):
        bundle.data['emis'] = bundle.obj.emis.id
        bundle.data['created_by'] = bundle.obj.created_by.id
        bundle.data['academic_level'] = bundle.obj.academic_level.id
        return bundle


class LearnerPerformanceDataCSVDownloadResource(CSVModelResource):
    """
    GET Learner Performance Data CSV
    ::

    "url": "<base_url>/api/v1/csv/data/learnerperformance/?username=name&api_key=key,
    "method": "GET",
    """
    emis = fields.ForeignKey("hierarchy.api.SchoolResource", 'emis')
    created_by = fields.ForeignKey(HeadTeacherResource, 'created_by')

    class Meta:
        queryset = LearnerPerformanceData.objects.all()
        resource_name = "csv/data/learnerperformance"
        list_allowed_methods = ['get']
        include_resource_uri = False
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()
        paginator_class = Paginator

    def dehydrate(self, bundle):
        bundle.data['emis'] = bundle.obj.emis.id
        bundle.data['created_by'] = bundle.obj.created_by.id
        return bundle


class InboundSMSCSVDownloadResource(CSVModelResource):
    """
    GET Inbound SMS CSV
    ::

    "url": "<base_url>/api/v1/csv/data/sms/?username=name&api_key=key,
    "method": "GET",
    """
    created_by = fields.ForeignKey(HeadTeacherResource, 'created_by')

    class Meta:
        queryset = InboundSMS.objects.all()
        resource_name = "csv/data/sms"
        list_allowed_methods = ['get']
        include_resource_uri = False
        serializer = CSVSerializer()  # Using custom serializer
        authentication = OverrideApiAuthentication()
        paginator_class = Paginator

    def dehydrate(self, bundle):
        bundle.data['created_by'] = bundle.obj.created_by.id
        return bundle
