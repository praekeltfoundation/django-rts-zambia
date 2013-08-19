from django.contrib import admin
from models import (Province, District, Zone, School)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ["emis", "name", "zone"]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(SchoolAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(zone__district=request.user.userdistrict.district_id)

admin.site.register(Province)
admin.site.register(District)
admin.site.register(Zone)
admin.site.register(School, SchoolAdmin)
