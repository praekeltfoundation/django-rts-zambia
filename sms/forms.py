from django.utils.translation import ugettext_lazy as _
from django import forms


class ChooseDistrictsForm(forms.Form):
    sms = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
    send_to_all = forms.BooleanField(label=_("All"), required=False)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop("queryset", None)
        super(ChooseDistrictsForm, self).__init__(*args, **kwargs)
        for query in queryset:
            self.fields["%s" % query.id ] = forms.BooleanField(label=query.name, required=False)

    def clean(self):
        cleaned_data = super(ChooseDistrictsForm, self).clean()

        data = dict((k, v) for k, v in cleaned_data.iteritems() if v and k != "sms")

        if "send_to_all" in data and len(data) > 1:
            raise forms.ValidationError(_("Choose all or specific districts not both"))

        return cleaned_data
