from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # Use your custom User model here
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('pic', 'name', 'bio')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself...',
                'rows': 5,
            }),
            'pic': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
        }
        labels = {
            'pic': 'Profile Picture',
            'name': 'Full Name',
            'bio': 'Short Bio',
        }