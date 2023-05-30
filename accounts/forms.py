from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Account

class SignUpForm(forms.ModelForm):

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
        "email_or_phone": _('please fill out phone number or email field.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    class Meta:
        model = Account
        fields = ["username", "phone_number", "email"]
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2
    
    def clean(self):
 
        super(SignUpForm, self).clean()
         
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone_number')
 
        if not email and not phone:
            self.add_error('email', _('please fill out phone number or email field.'))
            self.add_error('phone_number', _('please fill out phone number or email field.'))
        return self.cleaned_data
      
    def _post_clean(self):

        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ("avatar", "first_name", "last_name", "email", "phone_number")

    def clean(self):

        super(AccountForm, self).clean()

        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone_number')

        if not email and not phone:
            self.add_error('email', _('please fill out phone number or email field.'))
            self.add_error('phone_number', _('please fill out phone number or email field.'))
        return self.cleaned_data

