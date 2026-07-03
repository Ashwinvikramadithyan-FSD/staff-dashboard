from django import forms
from django.contrib.auth.hashers import make_password
from .models import Profile
from hr.models import BorrowRequest


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'dob',
                   'phone_number', 'email', 'role', 'password', 'confirm_password']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'dob-field'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if Profile.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already registered.")
        return username

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Password and Confirm Password must be the same.")
        return cleaned_data

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.password = make_password(self.cleaned_data['password'])
        if commit:
            profile.save()
        return profile


class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ['first_name', 'last_name', 'take_time', 'bring_time']
        widgets = {
            'take_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'bring_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }