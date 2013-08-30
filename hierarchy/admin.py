from django.contrib import admin
from models import (Province, District, Zone, School)
from rts.utils import DistrictIdFilter, ManagePermissions


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["name"]

    def get_actions(self, request):
        actions = super(ProvinceAdmin, self).get_actions(request)
        delete_perm = super(ProvinceAdmin, self).has_delete_permission(request)
        return ManagePermissions(parent=self,
                                 request=request,
                                 actions=actions,
                                 delete_perm=delete_perm).remove_delete_permission()


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "province"]

    def get_actions(self, request):
        actions = super(DistrictAdmin, self).get_actions(request)
        delete_perm = super(DistrictAdmin, self).has_delete_permission(request)
        return ManagePermissions(parent=self,
                                 request=request,
                                 actions=actions,
                                 delete_perm=delete_perm).remove_delete_permission()


class ZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "district"]

    def get_actions(self, request):
        actions = super(ZoneAdmin, self).get_actions(request)
        delete_perm = super(ZoneAdmin, self).has_delete_permission(request)
        return ManagePermissions(parent=self,
                                 request=request,
                                 actions=actions,
                                 delete_perm=delete_perm).remove_delete_permission()


class SchoolAdmin(admin.ModelAdmin):
    list_display = ["emis", "name", "zone"]


    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(SchoolAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


    def get_actions(self, request):
        actions = super(SchoolAdmin, self).get_actions(request)
        delete_perm = super(SchoolAdmin, self).has_delete_permission(request)
        return ManagePermissions(parent=self,
                                 request=request,
                                 actions=actions,
                                 delete_perm=delete_perm).remove_delete_permission()


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(School, SchoolAdmin)
