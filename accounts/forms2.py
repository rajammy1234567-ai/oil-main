from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-input'}),
        required=False,
        label='Create password',
        help_text='Leave blank to keep existing password. Minimum 8 characters.'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-input'}),
        required=False,
        label='Confirm password'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned = super().clean()
        p = cleaned.get('password')
        pc = cleaned.get('password_confirm')
        if p or pc:
            if p != pc:
                raise ValidationError('Passwords do not match.')
            if p and len(p) < 8:
                raise ValidationError('Password must be at least 8 characters long.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        if email:
            # keep username in sync with email so users can login with email
            user.username = email
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country']
