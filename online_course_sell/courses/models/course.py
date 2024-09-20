from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

class Course(models.Model):
    name = models.CharField(max_length=100,null=False)
    slug = models.CharField(max_length=100, null=True,  blank=True, unique=True)
    description = models.CharField(max_length=255, null=True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default=0)
    activate = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to="files/thumbnail")
    resource = models.FileField(upload_to="files/resource")
    length = models.IntegerField(null=False)
    
    def __str__(self):
        return self.name

class CourseProperty(models.Model):
    description = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(Course,null=False, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
        
        
class Tag(CourseProperty):
    pass

class Prerequisite(CourseProperty):
    pass

class Learning(CourseProperty):
    pass



def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    
    qs = Course.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        
pre_save.connect(pre_save_post_reciver, sender=Course)

    
