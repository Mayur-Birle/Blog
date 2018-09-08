from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name="Home"),
    path('ajax/like/',views.like,name="Like"),
    path('reg/',views.SignUp.as_view(),name="Reg"),
    path('reg',views.SignUp.as_view(),name="Reg"),
    path('create',views.CreateNew.as_view(),name="CreateNew"),
    path('login',views.LogIn.as_view(),name="LogIn"),
    path('logout/',views.logout,name="LogOut"),
    path('manage/',views.manage,name="Manage"),
    path('<int:author_id>/likedBloges',views.public_liked_view,name="LikeBlog"),
    path('<int:author_id>/',views.public_blog_view,name="PublicBlog"),
    path('<int:author_id>/<int:post_id>/',views.single_blog_view,name="SingleBlog"),
    path('<int:author_id>/<int:post_id>/edit',views.UpdateBlog.as_view(),name="UpdateBlog"),
    path('<int:author_id>/<int:post_id>/delete',views.delete_blog,name="DeleteBlog"),
]
