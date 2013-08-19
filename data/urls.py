from django.conf.urls import patterns, url, include
from data.api import (HeadTeacherResource, SchoolDataResource, InboundSMSResource,
                      TeacherPerformanceDataResource, LearnerPerformanceDataResource,
                      AcademicAchievementCodeResource)
from tastypie.api import Api


# Setting the API base name and registering the API resources using
# Tastypies API function
api_resources = Api(api_name='v1')
api_resources.register(HeadTeacherResource())
api_resources.register(SchoolDataResource())
api_resources.register(TeacherPerformanceDataResource())
api_resources.register(LearnerPerformanceDataResource())
api_resources.register(InboundSMSResource())
api_resources.register(AcademicAchievementCodeResource())
api_resources.prepend_urls()

# Setting the urlpatterns to hook into the api urls
urlpatterns = patterns('',
    url(r'^api/', include(api_resources.urls))
)
