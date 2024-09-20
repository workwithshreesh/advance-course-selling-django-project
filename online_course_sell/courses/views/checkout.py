from django.shortcuts import render, HttpResponse, redirect
from courses.models import Course, Payment, UserCourse, CouponCode
from online_course_sell.settings import *
from time import time
from random import randint, getrandbits
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

@login_required(login_url="/login")
def checkout_free(request,slug):
    course = Course.objects.get(slug = slug)
    user = request.user
    
    if course.discount is None or course.discount == 0:
        result = course.price
    else:
        sellprice = course.price
        sellprice = course.price - (course.price * course.discount * 0.01)
        result = float(int(sellprice))
    
    if result == 0:
        userCourse = UserCourse(user = user, course = course)
        userCourse.save()
        return redirect("enrolled_courses")
    
    return redirect("home")
    

@login_required(login_url="/login")
def checkout(request,slug):
    course = Course.objects.get(slug=slug)
    user = request.user
    action = request.GET.get('action')
    couponcode = request.GET.get('couponcode')
    coupon_code_message = None
    cupon = None
    order = None
    payment = None
    error = None
    amount = None
    
    try:
        user_course = UserCourse.objects.get(user= user, course = course)
        error = "You are Alredy Enrolled in this course"
    except:
        pass
    
    if couponcode:
        try:
            cupon = CouponCode.objects.get(course = course, code = couponcode)
            if cupon.discount == 100:
                userCourse = UserCourse(user = user, course = course)
                userCourse.save()
                return redirect("enrolled_courses")
            else:
                amount = int(course.price - (course.price * cupon.discount * 0.01))*100
                coupon_code_message = "Coupon applied successfully!"
        except:
            coupon_code_message = "Invalid Coupon Code. Please try again!"
            
                

    if error is None and amount is None:
        discounted_price = course.price * (1 - course.discount / 100)
        amount = int(discounted_price * 100)  # Convert to paise
        
        
    
    if action == 'create_payment':
        
            currency = 'INR'
            notes = {
                'email':user.email,
                'order': course.name
            }
            receipt = f"webname_{int(time())}_{randint(0,10000)}{chr(randint(ord('a'),ord('z')))}{randint(0,10000)}{chr(randint(ord('a'),ord('z')))}{getrandbits(32)}"
            order = client.order.create( { "amount": amount, 
                                            "currency": currency, 
                                            "receipt": receipt,
                                            "notes":notes })
            payment = Payment()
            payment.user = user
            payment.course = course
            payment.order_id = order.get("id")
            payment.save()
            
    
        
    context = {'courses':course,  'order':order, 
                   'payment':payment, 'user':user,
                   'error':error, 'coupon_code_message':coupon_code_message,
                   'cupon':cupon}
    return render(request,"courses/checkout.html",context)



@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = request.POST
        context = {}
        try:
            # params_dict = {
            #     'razorpay_order_id': data.get('razorpay_order_id'),
            #     'razorpay_payment_id': data.get('razorpay_payment_id'),
            #     'razorpay_signature': data.get('razorpay_signature')
            # }
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            
            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True
            
            userCourse = UserCourse(user = payment.user, course = payment.course)
            userCourse.save()
            
            payment.user_course = userCourse
            payment.save()
            
            return redirect("enrolled_courses")
        except:
            return HttpResponse("Invalid Payment Detail")
    