from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #inbuilt user of django
from .models import User # this is the custom user from our app
# Register your models here.

admin.site.register(User,UserAdmin)