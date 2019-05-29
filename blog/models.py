from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")

class Post(models.Model):
    objects = models.Manager()      # default manager
    
    published = PublishedManager()   # Custom model manager

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )



    title       =   models.CharField(max_length=250)
    slug        =   models.SlugField(max_length=250)
    author      =   models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body        =   models.TextField()
    likes       =   models.ManyToManyField(User, related_name='likes', blank=True)
    created     =   models.DateTimeField(auto_now_add=True)
    updated     =   models.DateTimeField(auto_now=True)
    status      =   models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id, self.slug])

@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True) 
    photo = models.ImageField(null=True, blank=True)


    def __str__(self):
        return "profile of User {}".format(self.user.username)