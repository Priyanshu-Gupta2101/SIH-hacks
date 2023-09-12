from django import forms
from .models import *

class PersonalDetailForm(forms.ModelForm):
    class Meta:
        model = PersonalDetail
        fields = "__all__"


class ContactDetailForm(forms.ModelForm):
    class Meta:
        model = ContactDetail
        fields = "__all__"


class GuardianDetailForm(forms.ModelForm):
    class Meta:
        model = GuardianDetail
        fields = "__all__"


class FileDetailForm(forms.ModelForm):
    class Meta:
        model = FileDetail
        fields = "__all__"

