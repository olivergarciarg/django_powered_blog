from django.contrib import admin
from .models import Post, Comment
# from .models import Post, Comment, UserProfileInfo


# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
# admin.site.register(UserProfileInfo)
