from django import forms
from .models import User,AssetRequest
from django.contrib.auth.password_validation import validate_password
import re
from .models import Asset

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "dob",
            "role",
            "branch",
            "password",
            "confirm_password",
        ]

        widgets = {
            "dob": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "dob-field"
                }
            )
        }

    # -----------------------
    # Username Validation
    # -----------------------

    def clean_username(self):

        username = self.cleaned_data["username"]

        if len(username) < 4:
            raise forms.ValidationError(
                "Username must contain at least 4 characters."
            )

        return username

    # -----------------------
    # First Name
    # -----------------------

    def clean_first_name(self):

        name = self.cleaned_data["first_name"]

        if not name.isalpha():
            raise forms.ValidationError(
                "First name should contain only letters."
            )

        return name

    # -----------------------
    # Last Name
    # -----------------------

    def clean_last_name(self):

        name = self.cleaned_data["last_name"]

        if not name.isalpha():
            raise forms.ValidationError(
                "Last name should contain only letters."
            )

        return name

    # -----------------------
    # Email Validation
    # -----------------------

    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists."
            )

        return email

    # -----------------------
    # Phone Number
    # -----------------------

    def clean_phone_number(self):

        phone = self.cleaned_data["phone_number"]

        if not phone.isdigit():
            raise forms.ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                "Phone number must be exactly 10 digits."
            )

        return phone

    # -----------------------
    # Branch
    # -----------------------

    def clean_branch(self):

        branch = self.cleaned_data["branch"]

        if self.cleaned_data["role"] == "STAFF" and not branch:
            raise forms.ValidationError(
                "Branch is required."
            )

        return branch

    # -----------------------
    # Password Validation
    # -----------------------

    def clean_password(self):

        password = self.cleaned_data.get("password")

        validate_password(password)

        return password

    # -----------------------
    # Confirm Password
    # -----------------------

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm:

            if password != confirm:

                self.add_error(
                    "confirm_password",
                    "Passwords do not match."
                )

        return cleaned_data
    
    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

        return user

class AssetRequestForm(forms.ModelForm):

    class Meta:
        model = AssetRequest
        fields = ['asset', 'reason']

class AssetForm(forms.ModelForm):

    class Meta:
        model = Asset

        fields = [
            'name',
            'description',
            'image',
            'is_in_stock'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Asset Name'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter Description'
            }),

            'is_in_stock': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }