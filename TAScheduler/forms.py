from django import forms


class EditAccountForm(forms.Form):
    first_name = forms.CharField(min_length=1, max_length=25, required=True)
    last_name = forms.CharField(min_length=1, max_length=25, required=True)
    address = forms.CharField(max_length=25, required=False)
    phone_number = forms.CharField(max_length=25, required=False)
    office_hours = forms.CharField(max_length=25, required=False)
