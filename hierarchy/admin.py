from django.contrib import admin
from models import (Province, District, Zone, School)
from rts.utils import DistrictIdFilter, ManagePermissions
from rts.actions import export_select_fields_csv_action



class ProvinceAdmin(ManagePermissions):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["name"]


class DistrictAdmin(ManagePermissions):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["name", "province"]


class ZoneAdmin(ManagePermissions):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["name", "district"]
    search_fields = ["name"]


class SchoolAdmin(ManagePermissions):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["emis", "name", "zone", "display_district", "display_province"]
    search_fields = ["emis"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "zone":
            kwargs["queryset"] = Zone.objects.order_by('name')
        return super(SchoolAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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
