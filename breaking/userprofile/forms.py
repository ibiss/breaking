from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from userprofile.models import UserProfile
import datetime

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label='Podaj imie')
    second_name = forms.CharField(max_length=100, required=True, label='Podaj nazwisko')
    latitude = forms.CharField(max_length=50, label='latitude')
    longitude = forms.CharField(max_length=50, label='longitude')
    
    class Meta:
        model = User
        fields = ("username","first_name","second_name","latitude","longitude",)

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UserCreateForm, self).save(commit=True)
        user_profile = UserProfile(user=user, first_name=self.cleaned_data['first_name'], second_name = self.cleaned_data['second_name'], status=True, latitude = self.cleaned_data['latitude'], longitude = self.cleaned_data['longitude'], timestamp=datetime.datetime.now())
        user_profile.save()
        return user, user_profile
