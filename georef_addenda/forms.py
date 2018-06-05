from django import forms
from georef_addenda.models import HelpFile


class HelpfileForm(forms.ModelForm):
    titol = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'5'}), required=True)
    h_file = forms.FileField(required=True)

    class Meta:
        model = HelpFile
        fields = ('titol','h_file',)