from django.shortcuts import render, redirect, get_object_or_404
from userAuth_profile.models import Profile
from userAuth_profile.forms.profile_form import ProfileForm

def change_profile(request):
    user = request.user
    # Fetch or initialize the user's profile
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        # Bind the form to POST data and FILES for file uploads
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Access cleaned data
            cleaned_data = form.cleaned_data
            name = cleaned_data.get('name')
            title = cleaned_data.get('title')
            desc = cleaned_data.get('desc')
            profile_img = cleaned_data.get('profile_img')
            
            # Update the profile instance with cleaned data
            profile.name = name
            profile.title = title
            profile.desc = desc
            profile.profile_img = profile_img
            profile.save()  # Save the updated profile

            return redirect('profile')  # Redirect to the profile page after saving
    else:
        # Initialize the form with the user's current profile instance
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {"form": form})
