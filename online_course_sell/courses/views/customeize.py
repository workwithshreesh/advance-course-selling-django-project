from django.shortcuts import render
from courses.models import SocialMediaLinks, SocialMediaTitle, AboutCategory, Contact, About
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings

#contact us page
def contact_us(request):
    # Render the contact form for GET requests
    contact = Contact.objects.all()
    context = {
        "contact": contact
    }
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Edited message format
        edited_message = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send email to the contact email specified in settings
        contact_email = settings.CONTACT_EMAIL

        # Create email message instance
        email_message = EmailMessage(subject, edited_message, to=[contact_email])
        
        # Send the email
        email_message.send()
        messages(request,"Email sended successfully!")
        # Optionally, you can return a success message or redirect
        
        return render(request, "courses/contact_us.html", context)

    return render(request, "courses/contact_us.html", context)





def about_us(request):
    about = About.objects.all()
    context ={"posts":about}
    
    return render(request,"courses/about.html",context)