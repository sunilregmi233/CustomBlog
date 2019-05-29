
from blog import views
from django.conf.urls import url
from django.urls import path, re_path


app_name = 'blog'
urlpatterns = [

    re_path(r'^blog/(?P<id>\d+)/(?P<slug>[\w-]+)/', views.post_detail, name="post_detail"),
    re_path('post_create/', views.post_create, name="post_create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
]
