from django.contrib import admin
from models import (Province, District, Zone, School)

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["name"]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "province"]


class ZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "district"]


class SchoolAdmin(admin.ModelAdmin):
    list_display = ["emis", "name", "zone"]


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(School, SchoolAdmin)
