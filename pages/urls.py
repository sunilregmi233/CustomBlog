from django.urls import path

from .views import HomePageView
from blog import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('blog/', views.post_list, name="post_list"),
]