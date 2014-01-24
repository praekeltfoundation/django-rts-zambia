from django.utils.translation import ugettext_lazy as _
from django import forms


class ChooseDistricsForms(forms.Form):
    send_to_all = forms.BooleanField(label="All", required=False)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop("queryset", None)
        super(ChooseDistricsForms, self).__init__(*args, **kwargs)
        for query in queryset:
            self.fields["district_%s" % query.id ] = forms.BooleanField(label=query.name, required=False)


class ChooseDistricsFormSet(forms.Form):
    district_id = forms.CharField(label=_(""), widget=forms.HiddenInput())
    send_to = forms.BooleanField(label="All", required=False)
