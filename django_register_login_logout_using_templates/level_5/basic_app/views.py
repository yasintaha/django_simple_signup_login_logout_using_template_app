from django.shortcuts import render
from basic_app.forms import form_user, User_profile_form
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse 
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def register(request):
    register = False

    if request.method == "POST":
        user_form = form_user(data=request.POST)
        profile_info = User_profile_form(data=request.POST)

        if user_form.is_valid() and profile_info.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_info.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']


            profile.save()

            register = True
        else:
            print(user_form.errors,profile_info.errors)

    else:
         user_form = form_user()
         profile_info = User_profile_form()

    return render(request,'basic_app/registration.html',{'user_form':user_form ,
                                                         'profile_form':profile_info,
                                                         'registered':register})     



def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        usr = authenticate(username=username,password=password)
        print(usr)
        if usr:
            if usr.is_active:
                login(request,usr)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("INVALID ACCOUNT")    
        else:
            print("some one tried ")
            print("Username:{} and Password:{}".format(username,password))
            return HttpResponse("INVALID DETAILS SUPPLIED")   

    else:
        return render(request,'basic_app/login.html',{})         

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))        

@login_required
def special(request):
    return  HttpResponse("Your logged in congrats")
