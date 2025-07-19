"""URLs for the Network app."""

# pylint: skip-file

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("viewprofile/<int:user_id>", views.viewprofile, name="viewprofile"),
    path("new_post", views.new_post, name="new_post"),
    path("following", views.following, name="following"),
    path("like/<int:post_id>", views.like, name="like"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("edit_post/", views.edit_post, name="edit_post"),
]
