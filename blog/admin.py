from django.contrib import admin
from .models import BlogModel, Tag, Category, Comment

admin.site.register(BlogModel)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
