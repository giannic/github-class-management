from django.db import models

from github import Github as Api

REPO_NAME_PATTERN = "hw_%s"
TEAM_NAME_PATTERN = "team_%s"


class MissingTeamException(Exception):
    """Thrown when we can't find the Github Team we need"""
    pass


class InvalidPullUrlException(Exception):
    """Thrown when the user provides an invalid pull request URL"""
    pass


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

        # First find the user
        # If this errors, we don't want to do other things
        new_user_github = api.get_user(new_user.profile.github_username)

        # Create the repo
        repo_name = REPO_NAME_PATTERN % new_user.username
        description = "Homework repository for %s" % new_user.username
        repo = org.create_repo(repo_name, description=description,
                               private=True)

        # Create the team, adding repo
        team_name = TEAM_NAME_PATTERN % new_user.username
        team = org.create_team(team_name, repo_names=[repo], permission="push")

        # Add the user to the team
        team.add_to_members(new_user_github)

        # Add the user to the 'students' team
        students_team = self.get_team('students')
        students_team.add_to_members(new_user_github)

        return repo

    def get_team(self, team_name):
        api, user, org = self.get_api()

        for team in org.get_teams():
            if team.name == team_name:
                return team

        #couldn't find the team
        raise MissingTeamException(team_name)

    def acknowledge_pull(self, submit_user, url):
        api, user, org = self.get_api()

        repo_name = REPO_NAME_PATTERN % submit_user.username
        repo = org.get_repo(repo_name)

        try:
            pull_number = int(url.split("/")[-1])
        except ValueError:
            raise InvalidPullUrlException(url)

        pull = repo.get_pull(pull_number)
        pull.create_issue_comment("Submission acknowledged.")
