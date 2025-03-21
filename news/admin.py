from django.contrib import admin
from .models import User, Category, Article, Comment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)

