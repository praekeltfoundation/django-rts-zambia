from django.contrib import admin
from models import (Province, District, Zone, School)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ["EMIS", "name", "zone"]

admin.site.register(Province)
admin.site.register(District)
admin.site.register(Zone)
admin.site.register(School, SchoolAdmin)
