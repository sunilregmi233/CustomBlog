from django.contrib import admin

# Register your models here.
from .models import Post

# place all the fields in admin Pannel
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status',)
    list_filter = ('status', 'created', 'updated')
    search_fields = ('author__username', 'title')
    prepopulated_fields = {"slug":('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')

admin.site.register(Post, PostAdmin)