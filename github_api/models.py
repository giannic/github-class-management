from django.db import models

from github import Github as Api


class Github(models.Model):
    """Connector to the Github API.

    Should only be one of these"""
    client_id = models.CharField(max_length=80)
    client_secret = models.CharField(max_length=80)

    org_name = models.CharField(max_length=50)
    gitignore_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50)
    token = models.CharField(max_length=80)

    def get_api(self):
        """Instantiate a PyGithub API object and get the associated org"""
        api = Api(self.token)
        user = api.get_user()
        org = api.get_organization(self.org_name)

        return (api, user, org)

    def create_repo(self, new_user):
        """Create a team and repo for a newly registered user"""
        api, user, org = self.get_api()

        # Create the repo
        repo_name = "%s_hw" % new_user.username
        description = "Homework repository for %s" % new_user.username
        repo = org.create_repo(repo_name, description=description,
                               private=True, auto_init=True,
                               gitignore_template="Python")

        # Create the team, adding repo
        team_name = "student_%s" % new_user.username
        team = org.create_team(team_name, repo_names=[repo], permission="push")

        # Add the user to the team
        new_user_github = api.get_user(new_user.profile.github_username)
        team.add_to_members(new_user_github)

        return repo
