from django import template
from courses.models import UserCourse
register = template.Library()


@register.simple_tag
def cal_sellprice(price, discount):
    if discount is None or discount is 0:
        return price
    sellprice = price
    sellprice = price - (price * discount * 0.01)
    return float(int(sellprice))

@register.filter
def rupee(price):
    return f"₹{price}"

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter
def percent(price):
    return f"{price}%"


@register.simple_tag
def is_enrolled(request, course):   
    
    user = None 
    if not request.user.is_authenticated:
        return False
    
    user = request.user
    try:
        user_course = UserCourse.objects.get(user = user, course = course)
        return True
    except:
        return False
    