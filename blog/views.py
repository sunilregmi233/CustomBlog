from django.shortcuts import render


from django.http import HttpResponse #new
from datetime import datetime

from .models import Post
# Create your views here.

# def index(request):
#     return HttpResponse("hello django")

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)