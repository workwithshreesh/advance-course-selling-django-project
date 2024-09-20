from django.shortcuts import render, HttpResponse, redirect
from courses.models import Course, Video, UserCourse
from django.contrib.auth.decorators import login_required

login_required(login_url="login")
def my_course(request):
    user= request.user
    user_course = UserCourse.objects.filter(user = user)
    context = {"courses":user_course}
    return render(request, "courses/mycourse.html", context)

def course(request,slug):
    course = Course.objects.get(slug=slug)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by('serial_number')
    
    next_lecture = 2
    previous_lecture = None
    first_lecture = 1
    last_lecture = len(videos)
    if serial_number is None:
        serial_number = 1
    else:
        next_lecture = int(serial_number)+1
        if len(videos) < next_lecture:
            next_lecture = None
        previous_lecture = int(serial_number)-1
        
        
    video = Video.objects.get(serial_number = serial_number, course = course)
    
    # check user are login and enrolled or not the course
    
    if ((request.user.is_authenticated is False) and (video.is_preview is False)):
        return redirect("login")
    
    if video.is_preview is False:
        
        if request.user.is_authenticated is False:
            return redirect("login")
        else:
            user = request.user
            try:
                user_course = UserCourse.objects.get(user= user, course = course)
            except:
                return redirect("checkout",slug=slug)
                
    
    context = {'courses':course,
               'video':video,
               'videos':videos,
               'first_lecture':first_lecture,'last_lecture':last_lecture,
               'next_lecture':next_lecture,'previous_lecture':previous_lecture}
    return render(request,"courses/course_page.html",context)