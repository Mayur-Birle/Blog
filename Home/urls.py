from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name="Home"),
    path('reg/',views.SignUp.as_view(),name="Reg"),
    path('reg',views.SignUp.as_view(),name="Reg"),
    path('login',views.LogIn.as_view()),
    path('logout/',views.logout,name="LogOut"),
]
