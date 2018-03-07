from django import forms
from material import *
from georef.models import *
from django.forms import ModelForm
from django.forms import inlineformset_factory
from datetimewidget.widgets import DateWidget
from georef_addenda.models import Profile


class ChangePasswordForm(forms.Form):
    password_1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    def clean_password_2(self):
        cleaned_data = self.cleaned_data
        password_2 = cleaned_data.get('password_2')
        password_1 = cleaned_data.get('password_1')
        if password_1 != password_2:
            raise forms.ValidationError('Els passwords són diferents! Si us plau torna a escriure\'ls')
        return password_2



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

    def clean_email(self):
        cleaned_data = self.cleaned_data
        proposed_email = cleaned_data.get('email')
        if User.objects.filter(email=proposed_email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Un altre usuari està fent servir aquest compte de correu, si us plau tria\'n un de diferent')
        return proposed_email


class NewUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

    def clean_email(self):
        cleaned_data = self.cleaned_data
        proposed_email = cleaned_data.get('email')
        if User.objects.filter(email=proposed_email).exists():
            raise forms.ValidationError('Un altre usuari està fent servir aquest compte de correu, si us plau tria\'n un de diferent')
        return proposed_email

    def clean_password(self):
        cleaned_data = self.cleaned_data
        password_2 = self.data['password_2']
        password_1 = cleaned_data.get('password')
        if password_1 != password_2:
            raise forms.ValidationError('Els passwords són diferents! Si us plau torna a escriure\'ls')
        return password_1


class ProfileForm(forms.ModelForm):
    permission_tesaure_edition = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    permission_administrative = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    permission_filter_edition = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    permission_toponim_edition = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    permission_recurs_edition = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Profile
        fields = ('toponim_permission', 'permission_tesaure_edition', 'permission_administrative', 'permission_filter_edition', 'permission_toponim_edition', 'permission_recurs_edition', )
        widgets = {
            'toponim_permission': forms.HiddenInput(),
        }