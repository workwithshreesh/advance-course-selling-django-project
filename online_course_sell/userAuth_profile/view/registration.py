from userAuth_profile.forms.register import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from random import randint
from datetime import timedelta
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse

def otp_genrator(): 
    return str(randint(100000,999999))

def send_otp_mail(email, otp):
    subject = "Your OTP for registration"
    message = render_to_string('otp_email.html', {'otp': otp})
    email = EmailMessage(subject, message, to=[email])
    email.content_subtype = 'html'
    email.send()

def register_view(request):
    if request.method == 'GET' and request.GET.get("myotp") == "generateotp":
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Please provide a valid email address to send OTP.'}, status=400)

        blocked_until_str = request.session.get('blocked-until')
        if blocked_until_str:
            blocked_until = parse_datetime(blocked_until_str)
            if blocked_until and timezone.now() < blocked_until:
                return JsonResponse({'status': 'error', 'message': 'You are temporarily blocked from generating OTP. Please try again later.'}, status=403)

        otp_attempts = request.session.get('otp_attempts', 0)
        if otp_attempts >= 6:
            request.session['blocked-until'] = (timezone.now() + timedelta(hours=8)).isoformat()
            request.session['otp_attempts'] = 0
            return JsonResponse({'status': 'error', 'message': 'Too many attempts. You are blocked for 8 hours.'}, status=429)

        otp = request.session.get('otp')
        otp_created_at_str = request.session.get('created_at')
        otp_created_at = parse_datetime(otp_created_at_str) if otp_created_at_str else None

        if otp and otp_created_at:
            time_elapsed = timezone.now() - otp_created_at
            if time_elapsed < timedelta(minutes=1):
                return JsonResponse({'status': 'error', 'message': 'Please wait for the OTP to expire before generating a new one.'}, status=429)
            elif time_elapsed > timedelta(minutes=1):
                return JsonResponse({'status': 'error', 'message': 'The otp is expired please try again !.'}, status=429)


        otp = otp_genrator()
        send_otp_mail(email, otp)
        request.session['otp'] = otp
        request.session['otp_email'] = email
        request.session['created_at'] = timezone.now().isoformat()
        request.session['otp_attempts'] = otp_attempts + 1

        return JsonResponse({'status': 'success', 'message': 'OTP sent successfully.'})

    # Handle POST request for registration
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data["confirm_password"]
            otp_verify = form.cleaned_data["otp_verify"]

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists, please try with another email.")
                return render(request, 'register_page.html', {'form': form})

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'register_page.html', {'form': form})

            if not request.session.get('otp') or request.session.get('otp_email') != email:
                messages.error(request, "Please generate and verify OTP before registering.")
                return render(request, 'register_page.html', {'form': form})

            if str(request.session.get('otp')) != otp_verify:
                messages.error(request, "Invalid OTP. Please try again.")
                return render(request, 'register_page.html', {'form': form})

            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            del request.session['otp']
            del request.session['otp_email']
            return redirect('login')
        else:
            messages.error(request, "Error in registration form.")
    
    form = RegistrationForm()
    return render(request, 'register_page.html', {'form': form})
