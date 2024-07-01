from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   path("signupform",views.signupform,name="signupform"),
    path ("signup",views.signup,name="signup"),
]
