from .course import Course
from django.db import models

class CouponCode(models.Model):
    #code course discount
    code = models.CharField(max_length=10)
    course = models.ForeignKey(Course,  on_delete=models.CASCADE, related_name='coupons')
    discount = models.IntegerField(default=0)
    start_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)