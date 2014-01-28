# Django
from django.conf.urls.defaults import patterns, url
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render
from django.contrib import admin
from django.db import models
from django import forms

# Project
from rts.utils import DistrictIdFilter, ManagePermissions
from rts.actions import export_select_fields_csv_action
from sms.models import SendSMS, SMSZones, TempSMSZones
from hierarchy.models import Zone, District
from sms.forms import ChooseDistricsForm
from sms.tasks import task_query_zone
from users.models import UserDistrict
from data.models import InboundSMS



"""
The Code below overides the TempZonelClass thus adding extra variables to it,
that will be used by form.ModelForm to auto generate the required zones
dynamically
"""
zones = Zone.objects.all()
zones_dict = dict((obj.id, obj.name) for obj in zones)

for key, value in zones_dict.iteritems():
    TempSMSZones.add_to_class(str(key), models.BooleanField(value))


class SMSZoneForm(forms.ModelForm):
    all = forms.BooleanField(label="All", required=False)

    class Meta:
        model = TempSMSZones
        exclude = ["zone",
                   "send_sms",
                   "num_sent"]


class SendSMSForm(forms.ModelForm):

    sms = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    class Meta:
        models = SendSMS
        exclude = ["total_sent",
                    "replies",
                   "user",
                   "district",
                   "created_at"]

    def __init__(self, *args, **kwargs):
        super(SendSMSForm, self).__init__(*args, **kwargs)


class SMSZoneFormset(BaseInlineFormSet):
    def clean(self):
        super(SMSZoneFormset, self).clean()

        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            data = dict((k, v) for k, v in form.cleaned_data.iteritems() if v)
            if "all" in data and len(data) > 2:
                raise forms.ValidationError("Choose all or specific zones not both")



class SMSZoneInline(admin.StackedInline):
    model = TempSMSZones
    form = SMSZoneForm
    formset = SMSZoneFormset
    max_num = 1

    def get_fieldsets(self, request, obj=None):
        fields_array = super(SMSZoneInline, self).get_fieldsets(request, obj=None)
        fields = fields_array[0][1]
        result = []
        temp = []
        if UserDistrict.objects.filter(user_id=request.user.id).exists():
            district = District.objects.get(id=request.user.userdistrict.district_id)
            zones = district.zone_set.all()
            query_dict = [temp.append(str(obj.id)) for obj in zones]

        for field in fields["fields"]:
            if field in temp:
                result.append(field)
        result.insert(0, "all")
        fields_array = [(None, {'fields': result})]
        return fields_array


class SendSMSAdmin(ManagePermissions):
    form = SendSMSForm
    inlines = [SMSZoneInline]
    list_display = ["sms", "created_by", "total_sent_messages", "replies", "district", "sent_to_all", "created_at"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]

    def __init__(self, *args, **kwargs):
        # Making sure somebody can't click already sent sms to edit it.
        super(SendSMSAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def has_add_permission(self, request):
        if self.is_district_admin(request) or self.is_rts_staff(request):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if self.is_district_admin(request) or self.is_rts_staff(request):
            return True
        return False

    def custom_save_zones(self, key, sms):
        """
        Repeated function to save zones
        """
        sms = SMSZones(send_sms=sms,
                        zone=Zone.objects.get(id=int(key)),
                        num_sent=50)
        sms.save()


    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Not allowing the user to change content once sent
        """
        return HttpResponseRedirect(reverse("admin:sms_sendsms_changelist"))

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.user = request.user
        obj.district_id = request.user.userdistrict.district_id
        obj.save()


    def save_related(self, request, form, formsets, change):
        """
        Overriding save related to save ro real database instead of the dummy database
        """
        form.save_m2m()
        for formset in formsets:
            if UserDistrict.objects.filter(user_id=request.user.id).exists():
                district = District.objects.get(id=request.user.userdistrict.district_id)
                zones = district.zone_set.all()
                temp = [str(obj.id) for obj in zones]

            result = {}
            for key, value in formset.cleaned_data[0].iteritems():
                if value:
                    result[key] = value

            for key, value in result.iteritems():
                if key.isdigit() and key in temp:
                    self.custom_save_zones(key, result["temp_sms"])
                    task_query_zone.delay(int(key), result["temp_sms"].sms)

                elif key == 'all':
                    for zone_id in temp:
                        self.custom_save_zones(zone_id, result["temp_sms"])
                        task_query_zone.delay(zone_id, result["temp_sms"].sms)

    def zones_view(self, request):
        pass

    def districts_view(self, request):
        """
            This is an internal custom admin view which is used to dynamically creates a send sms to districts form
            from which the RTS staff can send to selected indifiduals
        """
        if not self.is_rts_staff(request):
            messages.error(request, "You don't have the correct permissions to view this page")
            return HttpResponseRedirect(reverse("admin:index"))
        # Replicating views from django ModelAdmin
        model = self.model
        opts = model._meta

        # getting all the districts qs
        districts = District.objects.all()

        if request.method == "POST":
            district_form = ChooseDistricsForm(request.POST, queryset=districts)

            if district_form.is_valid():
                if district_form.cleaned_data["send_to_all"] == True:
                    # If all is selected, use the queryset
                    self.save_districts_zones_and_send_sms(request,
                                                           districts,
                                                           district_form.cleaned_data["sms"],
                                                           to_all=True)
                else:
                    # Iterating over the rest of the form IDs and checking if True and key is a digit
                    ids = [int(key) for key, value in district_form.cleaned_data.iteritems() if value and key.isdigit()]
                    districts_filtered = District.objects.filter(pk__in=ids).all()
                    self.save_districts_zones_and_send_sms(request, districts_filtered,
                                                           district_form.cleaned_data["sms"])

                messages.success(request, "The messages have been sent")
                return HttpResponseRedirect(reverse("admin:sms_sendsms_changelist"))
        else:
            district_form = ChooseDistricsForm(queryset=districts)
        context = {"title": "Send SMS to Headteachers in Districts",
                   "opts": opts,
                   "app_label": opts.app_label,
                   "district_form": district_form }
        return render(request,
                      "admin/sms/sendsms/districts_view.html",
                      context)

    def save_districts_zones_and_send_sms(self, request, districts_qs, sms, to_all=False):
        """This function gets the districts queryset and sms, then Creates a new SendSMS object,
            then saves it in SMSZones clas, after which sends to the celery worker which sends the sms
        """
        for district in districts_qs:
            sendsms = SendSMS.objects.create(sms=sms,
                                             district=district,
                                             user=request.user,
                                             sent_to_all=to_all)
            zones = district.zone_set.all()
            for zone in zones:
                self.custom_save_zones(zone.id, sendsms)
                task_query_zone.delay(zone.id, sendsms.sms)


    def add_view(self, request, form_url='', extra_context=None):
        if self.is_district_admin(request):
            return super(SendSMSAdmin, self).add_view(request, form_url='', extra_context=None)

        elif self.is_rts_staff(request):
            return HttpResponseRedirect(reverse("admin:sms_sendsms_districts_view"))

        else:
            # If not district_admin or rts_staff redirect back to the app with an error message
            # And extra security function.
            messages.error(request, "You don't have the correct permissions to view this page")
            return HttpResponseRedirect(reverse("admin:index"))


    def get_urls(self):
        urls = super(SendSMSAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'/admin/sms/sendsms/sms/zones', self.zones_view, name="sms_sendsms_zones_view"),
            url(r'/admin/sms/sendsms/sms/districts', self.districts_view, name="sms_sendsms_districts_view"))
        return my_urls + urls


    def is_district_admin(self, request):
        if UserDistrict.objects.filter(user_id=request.user.id).exists():
            return True
        return False

    def is_rts_staff(self, request):
        if not self.is_district_admin(request) and request.user.is_staff:
            return True
        return False


class InboundSMSProxy(InboundSMS):
    class Meta:
        proxy = True
        app_label = "sms"
        verbose_name = "Inbound SMS"
        verbose_name_plural = "Inbound SMS's"
        db_table = "Inbound SMS"

class InboundSMSAdmin(ManagePermissions):
    list_display = ["message", "created_by", "created_at"]
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]

    def queryset(self, request):
        """
        Limits queries for pages that belong to district admin
        """
        qs = super(InboundSMSAdmin, self).queryset(request)
        return DistrictIdFilter(parent=self, request=request, qs=qs).queryset()

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True


admin.site.register(SendSMS, SendSMSAdmin)
admin.site.register(SMSZones)
admin.site.register(InboundSMSProxy, InboundSMSAdmin)
