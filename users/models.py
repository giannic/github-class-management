from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    github_username = models.CharField(max_length=50)

User.profile = property(lambda u: UserProfile.objects.get(user=u)[0])
