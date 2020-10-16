from django import forms 
from microbrewforyou_app.models import BrewTypes


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=240)
    bio = forms.CharField(max_length=280)
    address = forms.CharField(max_length=280)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)


class EditUserForm(forms.Form):
    username = forms.CharField(max_length=240)
    first_name = forms.CharField(max_length=240)
    bio = forms.CharField(max_length=280)
    address = forms.CharField(max_length=280)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)


class PostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)


class PicForm(forms.ModelForm):

    class Meta:
        model = BrewTypes
        fields = ['name', 'averageABV', 'img_upload']