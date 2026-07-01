from django import forms
from .models import Profile, BorrowRequest 
from hr.models import BorrowRequest # Import both models directly

class Profile_Form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'dob', 'phone_number', 'email', 'role']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    # Note: Your clean method needs to be indented correctly under the class
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        if first_name and len(first_name) > 50:
            raise forms.ValidationError({'first_name': 'Name is too long!'})
        return cleaned_data

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ['first_name', 'last_name', 'take_time', 'bring_time']
        widgets = {
            'take_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'bring_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }