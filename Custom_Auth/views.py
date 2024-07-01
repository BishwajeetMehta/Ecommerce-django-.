from django.shortcuts import render,redirect
from django.http import HttpResponse
from Custom_Auth.models import User
from django.core.exceptions import ValidationError
# Create your views here.

def signupform(request):
    return HttpResponse(render(request,"signup.html"))

def signup(request):
    if request.method =="POST" :
        data = request.POST
        usertable = User()

        username = data.get("username")
        if username =="":
            raise ValidationError("User name cannot be null ")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        usertable.username = username 

        password = data.get("password")
        if password == "" :
             raise ValidationError("Password cannot be null ")
        if len(password) < 8:
            raise ValidationError("Password must be of 8 characters or more ")
        usertable.set_password(password)
        
        firstname = data.get("firstname")
        if firstname == "":
            raise ValidationError("firstname cannot be null ")
        usertable.first_name = firstname

        lastname = data.get("lastname")
        if lastname == "":
             raise ValidationError("lastname cannot be null ")
        usertable.last_name = lastname

        email = data.get("email")
        if email =="":
            raise ValidationError("Email cannot be null ")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        usertable.email = email

        phone = data.get("phone")
        if phone =="":
            raise ValidationError("Phone Number cannot be null ")
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("Phone Number already exists")
        usertable.phone =phone 

        usertable.DoB = data.get("DoB")
        usertable.image = data.get("image")
        usertable.save()
        
        return redirect("index")
    
    return redirect("signupform")