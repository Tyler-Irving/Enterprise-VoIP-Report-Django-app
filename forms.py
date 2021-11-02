from django import forms
from .models import ServiceLocationModel, NumberStatusModel, FilteredRateCentersModel

class InitialInfoForm(forms.Form):
    status_choices = tuple(NumberStatusModel.objects.values_list('value', 'description'))
    number_status = forms.CharField(label='Number Status ', widget=forms.Select(choices=status_choices))
    location_choices = tuple(ServiceLocationModel.objects.values_list('service_location_value', 'service_location_description'))
    location = forms.CharField(label='Location ', widget=forms.Select(choices=location_choices), initial="501005")

OPTIONS = [('1', 'YES'), ('0', 'NO'), ('2', 'ALL')]
class FilterRateCentersForm(forms.Form):
    rate_centers = forms.ChoiceField(choices=FilteredRateCentersModel.objects.all())
    port_in = forms.ChoiceField(label='Port In ', choices=OPTIONS, widget=forms.RadioSelect)

    def __init__(self, user, *args, **kwargs):
        super(FilterRateCentersForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['rate_centers'].choices = FilteredRateCentersModel.objects.filter(user=user).values_list('value', 'description').order_by('value')