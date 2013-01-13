from django.contrib import admin
from users.models import UserProfile
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = UserProfile


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]

admin.site.register(UserProfile)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
