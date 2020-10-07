from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=240)
    bio = forms.CharField(max_length=280)
    address = forms.CharField(max_length=280)
    city_choices = (
        ('Columbus', 'Columbus'),
        ('Colorado_Springs', 'Colorado Springs'),
        ('Carmel', 'Carmel')
    )
    state_choices = (
        ('Ohio', 'Ohio'),
        ('Colorado', 'Colorado')
    )
    city = forms.ChoiceField(choices=city_choices)
    state = forms.ChoiceField(choices=state_choices)


class PostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)
