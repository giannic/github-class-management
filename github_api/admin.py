from django.contrib import admin

from github_api.models import Github


class GithubAdmin(admin.ModelAdmin):
    """Special admin that prevents adding more than one github"""
    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        else:
            return True

admin.site.register(Github, GithubAdmin)
