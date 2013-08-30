from users.models import UserDistrict
from django.contrib import admin


class DistrictIdFilter:
    def __init__(self, parent=None, request=None, qs=None):
        self.request = request
        self.qs = qs
        self.parent = parent

    def queryset(self):
        if self.request.user.is_superuser:
            return self.qs
        elif UserDistrict.objects.filter(user_id=self.request.user.id).exists():
            emis_zone = ["SchoolDataAdmin", "HeadTeacherAdmin",
                         "TeacherPerformanceDataAdmin", "LearnerPerformanceDataAdmin"]
            created_by_emis = ["InboundSMSAdmin"]
            if self.parent.__class__.__name__ in emis_zone:
                return self.qs.filter(emis__zone__district=self.request.user.userdistrict.district_id)
            elif self.parent.__class__.__name__ in created_by_emis:
                return self.qs.filter(created_by__emis__zone__district=self.request.user.userdistrict.district_id)
            elif self.parent.__class__.__name__ == "SchoolAdmin":
                return self.qs.filter(zone__district=self.request.user.userdistrict.district_id)
        else:
            return self.qs


class ManagePermissions(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super(ManagePermissions, self).get_actions(request)
        delete_perm = super(ManagePermissions, self).has_delete_permission(request)
        if not delete_perm:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions