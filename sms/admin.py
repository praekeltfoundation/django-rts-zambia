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
from sms.models import SendSMS, SMSZones
from hierarchy.models import Zone, District
from sms.forms import ChooseDistricsForm, ChooseZonesForm
from sms.tasks import task_query_zone
from users.models import UserDistrict
from data.models import InboundSMS


class SendSMSAdmin(ManagePermissions):
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

    def zones_view(self, request):
        if not self.is_district_admin(request):
            messages.error(request, "You don't have the correct permissions to view this page")
            return HttpResponseRedirect(reverse("admin:index"))

        # Replicating views from django ModelAdmin
        model = self.model
        opts = model._meta

        district = District.objects.get(id=request.user.userdistrict.district_id)
        zones = district.zone_set.all()

        if request.method == "POST":
            zone_form = ChooseZonesForm(request.POST, queryset=zones)

            if zone_form.is_valid():
                if zone_form.cleaned_data["send_to_all"] == True:
                    self.save_zones_and_send_sms(request,
                                                 zones,
                                                 district,
                                                 zone_form.cleaned_data["sms"],
                                                 to_all=True)
                else:
                    # Iterating over the rest of the form IDs and checking if True and key is a digit
                    ids = [int(key) for key, value in zone_form.cleaned_data.iteritems() if value and key.isdigit()]
                    zones_filtered = Zone.objects.filter(pk__in=ids).all()
                    self.save_zones_and_send_sms(request,
                                                 zones_filtered,
                                                 district,
                                                 zone_form.cleaned_data["sms"])

                messages.success(request, "The messages have been sent")
                return HttpResponseRedirect(reverse("admin:sms_sendsms_changelist"))
        else:
            zone_form = ChooseZonesForm(queryset=zones)

        context = {"title": "Send SMS to Headteachers in Districts",
                   "opts": opts,
                   "app_label": opts.app_label,
                   "zone_form": zone_form }
        return render(request,
                      "admin/sms/sendsms/zones_view.html",
                      context)

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
            return each district zones and passes to the shared `run_save_zone_and_send_to_sms` fnc
        """
        for district in districts_qs:
            sendsms = SendSMS.objects.create(sms=sms,
                                             district=district,
                                             user=request.user,
                                             sent_to_all=to_all)
            zones_qs = district.zone_set.all()

            self.run_save_zone_and_send_to_sms(zones_qs, sendsms)


    def save_zones_and_send_sms(self, request, zones_qs, district_obj, sms, to_all=False):
        """This function gets the zones queryset and sms, then Creates a new SendSMS object,
            and passes to the shared `run_save_zone_and_send_to_sms` fnc
        """
        sendsms = SendSMS.objects.create(sms=sms,
                                         district=district_obj,
                                         user=request.user,
                                         sent_to_all=to_all)

        self.run_save_zone_and_send_to_sms(zones_qs, sendsms)


    def run_save_zone_and_send_to_sms(self, zones_qs, sendsms):
        for zone in zones_qs:
            self.custom_save_zones(zone.id, sendsms)
            task_query_zone.delay(zone.id, sendsms.sms)


    def add_view(self, request, form_url='', extra_context=None):
        if self.is_district_admin(request):
            return HttpResponseRedirect(reverse("admin:sms_sendsms_zones_view"))

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
            url(r'/admin/sms/sendsms/sms/districts', self.districts_view, name="sms_sendsms_districts_view"),
            url(r'/admin/sms/sendsms/sms/zones', self.zones_view, name="sms_sendsms_zones_view"),)
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
