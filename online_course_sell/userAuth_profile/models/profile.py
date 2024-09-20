from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default="Shreesh Tiwari (Default)", max_length=200, null=True)
    title = models.CharField(default="This is default title, change it in profile.", max_length=200, null=True)
    desc = models.CharField(default="Hey, there text description about you that you can change after clicking on 'Edit'", max_length=200, null=True)
    profile_img = models.ImageField(default='images/default.jpg', upload_to='images', null=True, blank=True)
    # forget_password_token = models.CharField(auto_now_add=True)

    def __str__(self):
        return self.name
