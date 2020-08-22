from django.contrib import admin
from .models import Post, Comment, Catogary

admin.site.register(Post)
admin.site.register(Catogary)
admin.site.register(Comment)
