from django.shortcuts import render, HttpResponse
from courses.models import Course

def home(request):
    course = Course.objects.filter(activate=True)
    return render(request,"courses/index.html",{'courses':course})