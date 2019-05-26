from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )



    title       =   models.CharField(max_length=250)
    slug        =   models.SlugField(max_length=250)
    author      =   models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body        =   models.TextField()
    created     =   models.DateTimeField(auto_now_add=True)
    updated     =   models.DateTimeField(auto_now=True)
    status      =   models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def __str__(self):
        return self.title