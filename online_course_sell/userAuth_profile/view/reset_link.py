from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_datetime



# The variables for validations of user attempts to send the link and expiry time of link
MAX_ATTEMPTS = 8
RESET_LINK_EXPIRY_MINUTES = 10



# Genrate a link and send to the user mail

def send_mail_reset(request):
    if request.method == 'POST':
        email_or_username = request.POST.get("id_email")
        
        if request.user.is_authenticated:
            messages.error(request,"You are alredy logged in.")
            return redirect("home")
        
        attempts = request.session.get("attempts",0)
        if attempts >= MAX_ATTEMPTS:
            messages.error(request, "Too many attempts. Please try again later.")
            return render(request, "send_resetlink.html")
        
        try:
            if '@' in email_or_username :
                email_username = User.objects.get(email = email_or_username)
            else:
                email_username = User.objects.get(username = email_or_username)
            
            if email_username:
                
                request.session["email_username"] = email_username.email
                request.session["created_at"] = timezone.now().isoformat()
                request.session["attempts"] = attempts + 1
                
                #Genrate tokenized reset link
                token = default_token_generator.make_token(email_username)
                uid = urlsafe_base64_encode(force_bytes(email_username.pk))
                reset_url = request.build_absolute_uri(reverse("changePassword",kwargs={'uidb64':uid,'token':token}))
                
                #send link on email
                subject = 'Password Reset Request'
                message = render_to_string('password_reset_email.html',{'user':email_username,
                                                                         'reset_url':reset_url})
                email = EmailMessage(subject,message,to=[email_username.email])
                email.content_subtype = 'html'
                email.send()
                messages.success(request,"Reset link sent on your email")
                
                
        except User.DoesNotExist:
            messages.error(request,"User does not exist")
    else:
        return render(request,"send_restlink.html")
            
    return render(request,"send_restlink.html")





#change the password of the user
def change_password(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        created_at_str = request.session.get('created_at')
        created_at = parse_datetime(created_at_str) if created_at_str else None
        if (timezone.now() - created_at) >= timedelta(minutes=RESET_LINK_EXPIRY_MINUTES):
            messages.error(request, "The password reset link has expired. Please request a new one.")
            return redirect('send_resetlink')
        
    except User.DoesNotExist:
        messages.error(request,"Invalid password reset link")
    
    if user is not None and default_token_generator.check_token(user,token):
        if request.method == 'POST':
            password = request.POST['password']
            if password == request.POST['confpassword']:
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password has been reset. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'change_password.html')
    else:
        messages.error(request, 'Invalid password reset link.')
        return redirect('SendResetLink')
