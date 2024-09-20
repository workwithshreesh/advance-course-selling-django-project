from django.db import models
from courses.models import UserCourse, Course
from django.contrib.auth.models  import User


class Payment(models.Model):
    order_id = models.CharField(max_length=80, null=False)
    payment_id = models.CharField(max_length=80)
    user = models.ForeignKey(User, null=False , on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=False , on_delete=models.CASCADE)
    user_course = models.ForeignKey(UserCourse, null = True, blank=True , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    