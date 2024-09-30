from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User 
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
        model = User  # Use your custom User model here as well
        fields = ('first_name', 'last_name','username', 'email' )
