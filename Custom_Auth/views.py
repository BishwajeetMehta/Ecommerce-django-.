from django.shortcuts import render,redirect
from django.http import HttpResponse
from Custom_Auth.models import User
from Product.models import System_setting
from django.contrib import messages
from django.core.mail import send_mail
import os
# Create your views here.

def signupform(request):
    return HttpResponse(render(request,"signup.html"))

def signup(request):
    if request.method =="POST" :
        data = request.POST
        usertable = User()

        username = data.get("username")
        if username =="":
            messages.error(request,"User name cannot be null ")
            return redirect("signupform")
           
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect("signupform")
        usertable.username = username 

        password = data.get("password")
        if password == "" :
            messages.error(request,"Password cannot be null ")
            return redirect("signupform")
        if len(password) < 8:
           messages.error(request,"Password must be of 8 characters or more ")
           return redirect("signupform")
        usertable.set_password(password)
        
        firstname = data.get("firstname")
        if firstname == "":
            messages.error(request,"firstname cannot be null ")
            return redirect("signupform")
        usertable.first_name = firstname

        lastname = data.get("lastname")
        if lastname == "":
            messages.error(request,"lastname cannot be null ")
            return redirect("signupform")
        usertable.last_name = lastname

        email = data.get("email")
        if email =="":
            messages.error(request,"Email cannot be null ")
            return redirect("signupform")
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect("signupform")
        usertable.email = email

        phone = data.get("phone")
        if phone =="":
            messages.error(request,"Phone Number cannot be null ")
            return redirect("signupform")
        if User.objects.filter(phone=phone).exists():
            messages.error(request,"Phone Number already exists")
            return redirect("signupform")
        usertable.phone =phone 

        DoB = data.get("DoB")
        if DoB =="":
            DoB = None
        usertable.DoB = DoB
        usertable.image = data.get("image")
        usertable.save()

        system_data= System_setting()
        subject = f' Registration Sucessful ! '
        message = f"Dear { usertable.username}, Your Registration is Sucessful !\n \n \n Thank you for choosing Us as your Shooping Partner !\n{system_data.slogan} "
        from_email = os.getenv("EMAIL_HOST")
        recipient_list = [usertable.email]
        send_mail(subject, message, from_email, recipient_list)
        
        return redirect("index")
    
    return redirect("signupform")