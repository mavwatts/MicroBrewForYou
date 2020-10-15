from django import forms
from microbrewforyou_app.models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name',
                  'bio', 'address', 'city', 'state']
    # username = forms.CharField(max_length=240)
    # password = forms.CharField(widget=forms.PasswordInput)
    # first_name = forms.CharField(max_length=240)
    # bio = forms.CharField(max_length=280)
    # address = forms.CharField(max_length=280)
    # city = forms.CharField(max_length=50)
    # state = forms.CharField(max_length=50)


class EditUserForm(forms.Form):
    username = forms.CharField(max_length=240)
    first_name = forms.CharField(max_length=240)
    bio = forms.CharField(max_length=280)
    address = forms.CharField(max_length=280)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)


class PostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)
