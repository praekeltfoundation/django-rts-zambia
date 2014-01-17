# Python
import csv
import StringIO

# Django
from django.contrib import admin


# Third Party
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.http import HttpUnauthorized

# Project
from users.models import UserDistrict


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


class CSVModelResource(ModelResource):
    def determine_format(self, request):
        return 'text/csv'

class CSVSerializer(Serializer):

    formats = ['csv']

    content_types = dict([('csv', 'text/csv')])

    def to_csv(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        raw_data = StringIO.StringIO()
        # import pdb; pdb.set_trace()
        if "objects" in data:
            if data['objects']:
                fields = data['objects'][0].keys()
                fields = [unicode(field).encode('utf-8') for field in fields]
                writer = csv.DictWriter(raw_data, fields,
                                        dialect="excel",
                                        extrasaction='ignore')
                header = dict(zip(fields, fields))
                writer.writerow(header)  # In Python 2.7: `writer.writeheader()`

                for item in data['objects']:
                    writer.writerow( {k: self.encode(v) for k, v in item.iteritems()})
        else:
            print data

        return raw_data.getvalue()

    def from_csv(self, content):
        raw_data = StringIO.StringIO(content)
        data = []
        # Untested, so this might not work exactly right.
        for item in csv.DictReader(raw_data):
            data.append(item)
        return data

    def encode(self, value):
        if isinstance(value, unicode):
            return value.encode("utf-8")
        return value


class OverrideApiAuthentication(ApiKeyAuthentication):
    def _unauthorized(self):
        data = "Sorry you are not authorized!"
        return HttpUnauthorized(content=data, content_type="text/plain; charset=utf-8")
