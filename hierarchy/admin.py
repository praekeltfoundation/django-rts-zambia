from django.contrib import admin
from models import (Province, District, Zone, School)
from rts.utils import DistrictIdFilter


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["name"]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "province"]


class ZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "district"]


class SchoolAdmin(admin.ModelAdmin):
    list_display = ["emis", "name", "zone"]


    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(SchoolAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(School, SchoolAdmin)
