from django import forms
from microbrewforyou_app.models import CustomUser, BrewTypes


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'user_image',
                  'bio', 'address', 'city', 'state']


class EditUserForm(forms.Form):
    username = forms.CharField(max_length=240)
    first_name = forms.CharField(max_length=240)
    bio = forms.CharField(max_length=280)
    address = forms.CharField(max_length=280)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    user_image = forms.ImageField()


class PostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)


class PicForm(forms.ModelForm):

    class Meta:
        model = BrewTypes
        fields = ['name', 'averageABV', 'img_upload']
