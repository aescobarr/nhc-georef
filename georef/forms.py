from django import forms
from material import *
from georef.models import *
from django.forms import ModelForm
from django.forms import inlineformset_factory

'''
class ToponimsForm(forms.Form):
    codi = forms.CharField(required=True)
    nom = forms.CharField(required=True)
    aquatic = forms.ChoiceField(choices=((None, ''), ('S', 'Sí'), ('N', 'No')))


    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=((None, ''), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')))
    receive_news = forms.BooleanField(required=False, label='I want to receive news and special offers')
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')



    layout = Layout(
        Row('codi', 'nom', 'aquatic'),
    )
'''

class ToponimsForm(forms.Form):
    codi = forms.CharField(required=True)
    nom = forms.CharField(required=True)
    aquatic = forms.ChoiceField(choices=((None, ''), ('S', 'Sí'), ('N', 'No')))
    idtipustoponim = forms.ModelChoiceField(queryset=Tipustoponim.objects.extra(order_by=['nom']))
    idpais = forms.ModelChoiceField(queryset=Pais.objects.extra(order_by=['nom']))
    idpare = forms.ModelChoiceField(queryset=Toponim.objects.all())


AQUATIC_CHOICES = (
    ('S','Sí'),
    ('N','No'),
)

class ToponimsUpdateForm(ModelForm):

    aquatic = forms.ChoiceField(choices=AQUATIC_CHOICES,widget=forms.RadioSelect, label='Aquàtic?')
    idtipustoponim = forms.ModelChoiceField(queryset=Tipustoponim.objects.all().order_by('nom'),widget=forms.Select, label='Tipus topònim')
    idpais = forms.ModelChoiceField(queryset=Pais.objects.all().order_by('nom'), widget=forms.Select, label='País')

    class Meta:
        model = Toponim
        exclude = ['id','codi', 'nom_fitxer_importacio', 'linia_fitxer_importacio']
        widgets = {
            'idpare': forms.HiddenInput(),
        }
