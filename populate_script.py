import os, django, random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from faker import Faker
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

 
def create_post(N):
    faker = Faker()
    for _ in range(N):
        id = random.randint(1,4)
        title = faker.name()
       
        Post.objects.create(title=title + " Post!!!",
        author = User.objects.get(id=id),
        status = random.choice(['published', 'draft']),
        slug = "-".join(title.lower().split()),
        body = faker.text(),
        created = timezone.now(),
        updated = timezone.now(),
        )

create_post(100)
print("DATA IS PPOPULATED SUCCESSFULLY")