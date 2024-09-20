from django.urls import path
from courses import views as course_views
from userAuth_profile import view as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', course_views.home, name='viewhome'),
    path('myprofile/', auth_views.home, name='profile'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register_view, name='register'),
    path('change-profile/', auth_views.change_profile, name='changeProfile'),
    path('send-reset-link/',auth_views.send_mail_reset,name="SendResetLink"),
    path('change-password/<uidb64>/<token>/',auth_views.change_password,name="changePassword"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
