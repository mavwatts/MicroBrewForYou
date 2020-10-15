from django import forms
from microbrewforyou_app.models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'user_image',
                  'bio', 'address', 'city', 'state']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'user_image',
                  'bio', 'address', 'city', 'state']


class PostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)
