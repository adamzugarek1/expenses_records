from django.urls import path
from .views import *
from . import views

urlpatterns = [path('login/', LoginUser.as_view(), name='login'),
               path('logout/', logout_user, name='logout'),
               path('register/', RegisterUser.as_view(), name='register'),
               path('rates/<slug:rates_slug>/', ShowRate.as_view(), name='post'),
               ]
