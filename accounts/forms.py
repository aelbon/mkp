# from allauth.account.forms import SignupForm  as MyAllauthBaseSignupForm # Note lowercase 'SignupForm'
from django import forms

class CustomSignupForm(forms.ModelForm): # Inherit from allauth's SignupForm
    # Add your custom fields here
    first_name = forms.CharField(max_length=30, required=True)  # Example
    last_name = forms.CharField(max_length=30, required=True)   # Example

    def __init__(self, args, *kwargs):
        super().__init__(*args, **kwargs)
        # Any other customization for form initialization
    def signup(self, request, user):
        return user
    def save(self, request, user, commit=True):
        user = super().save(request, user, commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user