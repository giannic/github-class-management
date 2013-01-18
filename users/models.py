from django.db import models
from django.contrib.auth.models import User

# http://www.turnkeylinux.org/blog/django-profile


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    github_username = models.CharField(max_length=50, unique=True)
    repo_url = models.CharField(max_length=80, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
