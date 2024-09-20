from django import template
from userAuth_profile.models import Profile

register = template.Library()

@register.simple_tag
def get_profile_name(user):
    """
    Retrieves the profile name for a given user.
    """
    try:
        profile = Profile.objects.get(user=user)
        return profile.name
    except Profile.DoesNotExist:
        return "No Name Found"

@register.simple_tag
def get_profile_title(user):
    """
    Retrieves the profile title for a given user.
    """
    try:
        profile = Profile.objects.get(user=user)
        return profile.title
    except Profile.DoesNotExist:
        return "No Title Found"

@register.simple_tag
def get_profile_desc(user):
    """
    Retrieves the profile description for a given user.
    """
    try:
        profile = Profile.objects.get(user=user)
        return profile.desc
    except Profile.DoesNotExist:
        return "No Description Found"


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})