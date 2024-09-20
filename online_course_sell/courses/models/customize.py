from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

class SocialMediaTitle(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=255, null=True)
    icon = models.ImageField(upload_to="customImage/SocialIcons", null=False)

    def __str__(self):
        return self.name

class SocialMediaLinks(models.Model):
    title = models.ForeignKey(SocialMediaTitle, on_delete=models.CASCADE)
    url = models.URLField(max_length=400, null=False)

    def __str__(self):
        return self.url

class AboutCategory(models.Model):
    category = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.category

class About(models.Model):
    category = models.ForeignKey(AboutCategory, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, null=False, blank=True)
    thumbnail = models.ImageField(upload_to="customImage/thumbnail", null=False)

    def __str__(self):
        return self.title

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = About.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=About)

class Contact(models.Model):
    address = models.TextField()
    email = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=14)  # Changed to CharField to support formatting like dashes or spaces
    map_id = models.TextField()  # Assuming this holds some map embed ID or script
    office_hours = models.TextField()  # Added to specify office hours

    def __str__(self):
        return f"Contact Info - {self.email}"
