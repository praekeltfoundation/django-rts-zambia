from django.contrib import admin
from models import (Provinces, Districts, Zones, Schools)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ["EMIS", "name", "zone_id"]

admin.site.register(Provinces)
admin.site.register(Districts)
admin.site.register(Zones)
admin.site.register(Schools, SchoolAdmin)