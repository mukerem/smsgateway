from django import forms
from .models import User
from django.contrib.auth.hashers import check_password
from account.validators import phone_number_validator

class EditMyProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'register_date']
        widgets = {
            'email': forms.TextInput(attrs={'readonly': True}),
            'register_date': forms.DateInput(attrs={'readonly': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if (not first_name) or (not last_name):
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data


class EditUserProfile(forms.ModelForm):

    class Meta:
        model = User
        exclude = ['password', 'role', 'last_login', 'is_active']
        widgets = {
            'register_date': forms.DateInput(attrs={'readonly': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        email = cleaned_data.get('email')
        last_name = cleaned_data.get('last_name')
        if (not last_name) or (not last_name) or (not email):
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data


class AddUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        role = cleaned_data.get('role')
        email = cleaned_data.get('email')

        if (not first_name) or (not last_name) or (not role) or (not email):
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data


class CSVUserUpload(forms.Form):
    file = forms.FileField(
        label='csv',
        widget=forms.FileInput(),
        help_text='* choose csv file.'

    )


class ChangePassword(forms.Form):
    def __init__(self, *args, **kwargs):
        self.password = kwargs.pop('password', None)
        super(ChangePassword, self).__init__(*args, **kwargs)

    old_password = forms.CharField(
        max_length=1024,
        widget=forms.PasswordInput(),
    )
    password_regex = phone_number_validator
    new_password = forms.CharField(
        label='New password:',
        validators=[password_regex],
        max_length=1024,
        widget=forms.PasswordInput(),
        help_text='minimum 6 character'
    )
    confirm = forms.CharField(
        label='New password confirmation:',
        max_length=1024,
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm')
        if (not old_password) or (not new_password) or (not confirm_password):
            raise forms.ValidationError("Please correct the errors below.")

        if check_password(old_password, self.password):
            if new_password:
                if new_password == confirm_password:
                    return
                else:
                    raise forms.ValidationError("password is not confirmed")
        else:
            raise forms.ValidationError(
                "Your old password was entered incorrectly. Please enter it again.")

        return cleaned_data
