from django import forms
from django.contrib.auth.models import User
from userAuth_profile.models.profile import Profile  # Ensure this import matches your actual model location

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'title', 'desc', 'profile_img']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Title'}),
            'desc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'profile_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }
    
    def __init__(self, *args, **kwargs):
        # You can customize the form further here if needed
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['title'].required = False
        self.fields['desc'].required = False
        self.fields['profile_img'].required = False
