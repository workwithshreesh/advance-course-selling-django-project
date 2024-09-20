from django.shortcuts import render
from userAuth_profile.models.profile import Profile
def home(request):
    user = request.user
    # profile = Profile.objects.all()
    return render(request,'home.html',{"user":user})