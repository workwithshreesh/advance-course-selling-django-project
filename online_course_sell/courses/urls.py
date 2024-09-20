from django.urls import path
from courses.views import home, course, SignupView, LoginView, singout, checkout, verify_payment, my_course, checkout_free
from courses.views import contact_us, about_us
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name="home"),
    # path('signup/',SignupView.as_view(),name = 'signup'),
    # path('login/',LoginView.as_view(), name = 'login'),
    # path('logout/',singout,name= 'logout'),
    path('enrolled_courses/',my_course,name= 'enrolled_courses'),
    path('check_out_free/<slug:slug>',checkout_free, name = 'checkout_free'),
    path('course/<slug:slug>',course,name = 'course'),
    path('check-out/<slug:slug>',checkout,name = 'checkout'),
    path('verify_payment',verify_payment,name = 'verify_payment'),
    path('contact-us/', contact_us ,name="contactUs"),
    path('about-us/', about_us ,name="aboutUs"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
