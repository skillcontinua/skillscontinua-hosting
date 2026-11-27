# C:\hosting\skillscontinua_hosting\village\urls.py
from django.urls import path
from . import views

app_name = "village"

urlpatterns = [
    path("", views.village_home, name="home"),
    path("blog/", views.post_list, name="post_list"),
    path("blog/<slug:slug>/", views.post_detail, name="post_detail"),
    path("media/", views.media_list, name="media_list"),
    path("forum/", views.forum_list, name="forum_list"),
    path("forum/<slug:slug>/", views.forum_detail, name="forum_detail"),
]
