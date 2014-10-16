from django.contrib import admin
from models import (Province, District, Zone, School)
from rts.utils import DistrictIdFilter, ManagePermissions
from rts.actions import export_select_fields_csv_action


class MyDistrictAdminForm(forms.ModelForm):



class ProvinceAdmin(ManagePermissions):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["name"]


class DistrictAdmin(ManagePermissions):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["name", "province"]


class ZoneAdmin(ManagePermissions):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["name", "district"]


class SchoolAdmin(ManagePermissions):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["emis", "name", "zone", "display_district", "display_province"]
    search_fields = ["emis"]


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
