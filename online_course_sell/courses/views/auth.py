from django.shortcuts import render, HttpResponse, redirect
# from django.contrib.auth.forms import UserCreationForm
from courses.forms import RegistrationForm, LoginForm
from django.views import View
from django.contrib.auth import logout, login

class SignupView(View):
    def get(self, request):
        if (request.method == 'GET'):
            form = RegistrationForm()
            return render(request,"courses/signup.html",{'form':form})
    
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if (user is not None):
                return redirect('login')  
        
        return render(request,"courses/signup.html",{'form':form})
    

    
              

    

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form':form
        }
        return render(request, "courses/login.html",context=context)
    
    def post(self, request):
        form = LoginForm(request=request, data = request.POST)
        if (form.is_valid()):
            user = form.get_user()
            login(request, user)
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('home')
        context = {
            'form':form
        }
        return render(request, "courses/login.html",context=context)



def singout(request):
    logout(request)
    return redirect('home')