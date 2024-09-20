# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from userAuth_profile.forms import LoginForm
from django.contrib import messages
from django.urls import reverse

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Determine if the input is an email or username
            if '@' in username_or_email:
                # Try to fetch the user by email
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    username = user_obj.username
                except User.DoesNotExist:
                    messages.error(request, "Invalid email or password.")
                    return render(request, 'login_page.html', {'form': form})
            else:
                # Input is considered a username
                username = username_or_email

            # Authenticate the user with the determined username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your home or dashboard
            else:
                messages.error(request, "Invalid username/email or password.")
        else:
            messages.error(request, "Form is not valid.")
    else:
        form = LoginForm()

    return render(request, 'login_page.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')