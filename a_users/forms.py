from django import forms
from django.forms import ModelForm
from .models import *


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        labels = {
            'realname': 'Name'
        }

        widgets = {
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows':3})
        }