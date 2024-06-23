from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('register/', views.Register.as_view(), name="register"),
    path('home/', views.Home.as_view(), name="home"),
    path('adminhome/', views.AdminHome.as_view(), name="adminhome"),
    path('events/', views.EventList.as_view(), name='event_list'),
    path('addevent/', views.CreateEvent.as_view(), name='addevent'),
    path('registration/<str:id>', views.RegisterEvent.as_view(), name='registration'),
    path('delete/<id>', views.Delete.as_view(), name='registration'),
    path('update/<id>', views.Update.as_view(), name='registration'),
    
    
   
]
