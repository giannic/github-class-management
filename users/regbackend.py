from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from registration.backends.simple import SimpleBackend
from registration import signals

from forms import CustomRegistrationForm

from github_api.models import Github


class CustomBackend(SimpleBackend):
    def register(self, request, **kwargs):
        """
        Create and immediately log in a new user.

        """
        username, email, password = (kwargs['username'], kwargs['email'],
                                     kwargs['password1'])
        user = User.objects.create_user(username, email, password)

        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']

        user.save()

        try:
            #profile stuff
            github_username = kwargs['github_username']
            profile = user.profile
            profile.github_username = github_username
            profile.save()

            gh = Github.objects.get()
            repo = gh.create_repo(user)
            profile.repo_url = repo.url

            profile.save()

        except Exception as e:
            #need to delete the already created user
            user.delete()
            raise e

        # authenticate() always has to be called before login(), and
        # will return the user we just created.
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get_form_class(self, request):
        return CustomRegistrationForm
