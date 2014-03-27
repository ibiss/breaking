from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from userprofile.models import UserProfile
import datetime

class UserCreateForm(UserCreationForm):
    latitude = forms.CharField(max_length=50, label='latitude')
    longitude = forms.CharField(max_length=50, label='longitude')
    avatar = forms.ImageField()
    class Meta:
        model = User
        fields = ("username","first_name","last_name","latitude","longitude","avatar",)

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UserCreateForm, self).save(commit=True)
        user_profile = UserProfile(
		user = user,
		latitude = self.cleaned_data['latitude'],
		longitude = self.cleaned_data['longitude'],
		points = 0,
		rank_points = 0,
		count_rock = 0,
		count_gold = 0,
		count_wood = 0,
		avatar = self.cleaned_data['avatar'],
		base_level = 1)
        user_profile.save()
        return user, user_profile

class FromTo(forms.Form):
    rfrom = forms.IntegerField(initial=2,min_value=2,max_value=100)
    rto = forms.IntegerField(initial=3,min_value=3,max_value=101)

class UserUpdateForm(forms.Form):
    latitude = forms.CharField(max_length=50, label='latitude')
    longitude = forms.CharField(max_length=50, label='longitude')
    first_name = forms.CharField(max_length=50, label='Imie')
    last_name = forms.CharField(max_length=50, label='Nazwisko')
    email = forms.CharField(max_length=50, label='Email')
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['first_name', 'last_name', 'email', 'latitude', 'longitude']
class CommunicatorForm(forms.Form):
	description = forms.CharField(required=True, widget=forms.Textarea, label='wiadomosc',
		error_messages={'required': 'Wpisz jakas wartosc!!'})
