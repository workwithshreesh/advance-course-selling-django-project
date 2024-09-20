from django.contrib import admin
from django.utils.html import format_html
from courses.models import Course, Tag, Prerequisite, Learning, Video, UserCourse, Payment, CouponCode, SocialMediaLinks, SocialMediaTitle, About, AboutCategory, Contact

class TagAdmin(admin.TabularInline):
    model = Tag
    
class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite
    
class LearningAdmin(admin.TabularInline):
    model = Learning
    
class VideoAdmin(admin.TabularInline):
    model = Video
    
    
# Main Course model admin
class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, PrerequisiteAdmin, LearningAdmin, VideoAdmin]
    
    list_display = ['name','get_price','get_discount','activate']
    list_filter = ('discount','activate')
    actions = ['activate_courses',]
    
    def get_discount(self,Course):
        return f"{Course.discount} %"
    
    def get_price(self,Course):
        return f"₹ {Course.price}"
    
    def activate_courses(self, request, queryset):
        """Admin action to activate selected courses."""
        updated = queryset.update(activate=True)
        self.message_user(request, f"{updated} course(s) successfully activated.")
    
    
    activate_courses.short_description = 'Active'
    get_price.short_description = 'Price'
    get_discount.short_description = 'Discount'


# Payment detail admin model
class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['order_id','get_user','get_course','status']
    list_filter = ['status','course']
    
    def get_user(self, payment):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{payment.user.id}'>{payment.user}</a>")
    
    def get_course(self, payment):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{payment.course.id}'>{payment.course}</a>")
    
    get_course.short_description = 'Course'
    get_user.short_description = 'User'
    
    
# User Course Enroll admin model
class UserCourseAdmin(admin.ModelAdmin):
    model = UserCourse
    list_display = ['Click','get_user','get_course']
    list_filter = ['course']
    
    def Click(self, usercourse):
        return "Click to Open"
    
    def get_user(self, usercourse):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{usercourse.user.id}'>{usercourse.user}</a>")
    
    def get_course(self, usercourse):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{usercourse.course.id}'>{usercourse.course}</a>")
    
    get_course.short_description = 'Course'
    get_user.short_description = 'User'
    

    # Videos Model
class VideoAdmin(admin.ModelAdmin):
    model = UserCourse
    list_display = ['Click','title','get_course','is_preview']
    list_filter = ['course',]
    
    def Click(self, video):
        return "Click to Open"
    
    def get_course(self, video):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{video.course.id}'>{video.course}</a>")
    
    get_course.short_description = 'Course'
    


# Coupon Code admin model
class CouponCodeAdmin(admin.ModelAdmin):
    model = CouponCode
    list_display = ['Click','code','get_course','get_discount']
    list_filter = ['course',]
    
    def Click(self, coupon):
        return "Click to Open"
    
    def get_discount(self, coupon):
        return f"{coupon.discount} %"
    
    def get_course(self, coupon):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{coupon.course.id}'>{coupon.course}</a>")
    
    get_course.short_description = 'Course'
    get_course.short_description = 'Discount'
    
    
    
    
class AboutModel(admin.ModelAdmin):
    model = About
    list_display = ["category","title","content","slug","thumbnail"]
    list_filter = ["category"]
    
    def get_category(self, about):
        return format_html(f"<a target='_blank' href='/admin/courses/aboutcategory/{about.category.id}'>{about.category}</a>")
    
    get_category.short_description = 'Category'
    
# class AboutCategoryModel(admin.ModelAdmin):
#     model = AboutCategory
#     list_display = ["category"]

class AboutCategoryModel(admin.ModelAdmin):
    model = AboutCategory
    list_display = ["category"]


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ["address","email","phone_num","map_id","office_hours"]

class SocialTitle(admin.ModelAdmin):
    model = SocialMediaTitle
    list_display = ["name","description","icon"]
    
class SocialLinks(admin.ModelAdmin):
    model = SocialMediaLinks
    list_display = ["title","url"]



    
admin.site.register(Course, CourseAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(CouponCode, CouponCodeAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(About,AboutModel)
admin.site.register(AboutCategory, AboutCategoryModel) 
admin.site.register(SocialMediaTitle,SocialTitle)
admin.site.register(SocialMediaLinks,SocialLinks)
