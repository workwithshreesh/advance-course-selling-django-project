from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=45, required=True)
    last_name = forms.CharField(max_length=80, required=True)
    email = forms.EmailField(max_length=200, required=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']
        
        # widgets = {
        #     'first_name' : forms.TextInput(attrs={'class':'form-control'}),
        #     'last_name' : forms.TextInput(attrs={'class':'form-control'}),
        #     'username' : forms.TextInput(attrs={'class':'form-control'}),
        #     'email' : forms.EmailInput(attrs={'class':'form-control'}),
        # }
        
    
    def clean_email(self):
        email  = self.cleaned_data['email']
        user = None
        
        try:
            user = User.objects.get(email)
        except:
            return email
        
        if user is not None:
            raise ValidationError("Email is alredy exist!")
        
        