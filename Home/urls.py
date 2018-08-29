from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name="Home"),
    path('reg/',views.SignUp.as_view(),name="Reg"),
    path('reg',views.SignUp.as_view(),name="Reg"),
    path('create',views.CreateNew.as_view(),name="CreateNew"),
    path('login',views.LogIn.as_view(),name="LogIn"),
    path('logout/',views.logout,name="LogOut"),
    path('<int:author_id>/',views.public_blog_view,name="PublicBlog"),
    path('<int:author_id>/<int:post_id>/',views.single_blog_view,name="SingleBlog"),
]
