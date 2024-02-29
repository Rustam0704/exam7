import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import User, Item, Category


class LoginForm(forms.Form):
    username = forms.CharField(max_length=256, widget=forms.TextInput(attrs={"class": "form-control", "id": "username", "placeholder": "username", "maxlength": "256"}))
    password = forms.CharField(max_length=256, widget=forms.TextInput(attrs={"class": "form-control", "id": "password", "type": "password", "placeholder": "password"}))


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=28, widget=forms.TextInput(
        attrs={"id": "password", "type": "password"}))
    password2 = forms.CharField(max_length=28, widget=forms.TextInput(
        attrs={"id": "password", "type": "password"}))
    avatar = forms.FileField()

    def save(self, commit=True):
        user = super().save(commit)
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 == password2:
            user.set_password(password1)
            user.save()
        else:
            raise ValidationError("Passwords must be match")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2", "email", 'avatar')

class ItemCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                    {"class": "form-control", "placeholder": f"Enter the {str(field)}"})

    class Meta:
        model = Item
        fields = ("title", "description", "price", 'category','ends_in','owner_name', 'owner_username', 'image')


class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("title", "description", "price", 'category','ends_in','owner_name', 'owner_username', 'image')
