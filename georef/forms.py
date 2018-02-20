from django import forms
from material import *
from georef.models import *
from django.forms import ModelForm
from django.forms import inlineformset_factory
from datetimewidget.widgets import DateWidget
from georef_addenda.models import Profile

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
    aquatic = forms.ChoiceField(choices=AQUATIC_CHOICES,widget=forms.RadioSelect, label='Aquàtic?', required=False)
    idtipustoponim = forms.ModelChoiceField(queryset=Tipustoponim.objects.all().order_by('nom'),widget=forms.Select, label='Tipus topònim')
    idpais = forms.ModelChoiceField(queryset=Pais.objects.all().order_by('nom'), widget=forms.Select, label='País', required=False)

    class Meta:
        model = Toponim
        exclude = ['id','codi', 'nom_fitxer_importacio', 'linia_fitxer_importacio']
        widgets = {
            'idpare': forms.HiddenInput(),
        }


class ToponimversioForm(ModelForm):
    numero_versio = forms.IntegerField(required=True)
    idqualificador = forms.ModelChoiceField(queryset=Qualificadorversio.objects.all().order_by('qualificador'), widget=forms.Select, required=False)
    idrecursgeoref  = forms.ModelChoiceField(queryset=Recursgeoref.objects.all().order_by('nom'), widget=forms.Select, required=False)
    coordenada_x_centroide = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False)
    coordenada_y_centroide = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False)
    precisio_h = forms.FloatField(widget=forms.NumberInput(attrs={'readonly':'readonly'}), required=False)
    dateTimeOptions = {
        'format': 'dd/mm/yyyy'
    }
    datacaptura = forms.DateField(initial=datetime.date.today, input_formats=['%d/%m/%Y'],widget=DateWidget(bootstrap_version=3, options=dateTimeOptions))

    class Meta:
        model = Toponimversio
        fields = ['numero_versio', 'idqualificador','idrecursgeoref','nom','datacaptura','coordenada_x_origen','coordenada_y_origen','coordenada_z_origen','precisio_z_origen','coordenada_x_centroide','coordenada_y_centroide','precisio_h']


class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class ProfileForm(forms.ModelForm):
    permission_visualize = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    permission_administrative = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    permission_filter_edition = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    class Meta:
        model = Profile
        fields = ('toponim_permission', 'permission_visualize', 'permission_administrative', 'permission_filter_edition', )