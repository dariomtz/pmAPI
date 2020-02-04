from django import forms
from django.contrib.auth.models import User

class UserRegistration(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("That email is already being used for a different user.", code='unique')
        return email

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]

class UserEditProfile(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username = username).exists():
            raise forms.ValidationError("That email is already being used for a different user.", code='unique')
        return email

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]

class UserChangePassword(forms.ModelForm):
    old_password = forms.CharField(required=True)

    def clean_old_password(self):
        username = self.cleaned_data.get('username')

        user = User.objects.get(username=username)
        old_password = self.cleaned_data.get('old_password')

        if not user.check_password(old_password):
            raise forms.ValidationError("Incorrect old password.", code='invalid')
        return self.cleaned_data
        

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    