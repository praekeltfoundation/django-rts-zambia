from django.conf.urls import patterns, url, include
from data import api
from tastypie.api import Api


# Setting the API base name and registering the API resources using
# Tastypies API function
api_resources = Api(api_name='v1')

api_resources.register(api.DistrictAdminResource())
api_resources.register(api.HeadTeacherResource())
api_resources.register(api.SchoolDataResource())
api_resources.register(api.TeacherPerformanceDataResource())
api_resources.register(api.LearnerPerformanceDataResource())
api_resources.register(api.InboundSMSResource())
api_resources.register(api.AcademicAchievementCodeResource())


api_resources.register(api.HeadTeacherCSVDownloadResource())
api_resources.register(api.SchoolDataCSVDownloadResource())
api_resources.register(api.TeacherPerformanceDataCSVDownloadResource())
api_resources.register(api.LearnerPerformanceDataCSVDownloadResource())
api_resources.register(api.InboundSMSCSVDownloadResource())
api_resources.register(api.AcademicAchievementCodeCSVDownloadResource())


api_resources.prepend_urls()

# Setting the urlpatterns to hook into the api urls
urlpatterns = patterns('',
    url(r'^api/', include(api_resources.urls))
)
