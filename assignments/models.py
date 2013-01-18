from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User


class Assignment(models.Model):
    """An assignment description"""
    number = models.IntegerField()
    due_date = models.DateTimeField()
    name = models.CharField(max_length=80)
    url = models.URLField(blank=True)
    max_correctness_grade = models.IntegerField(blank=True, null=True)
    max_style_grade = models.IntegerField(blank=True, null=True)
    submissions_open = models.BooleanField()

    def __unicode__(self):
        return "Assignment %(number)d" % self.__dict__

    @property
    def total_submissions(self):
        return self.submission_set.count()


class Submission(models.Model):
    """An individual student's submission of an assignment.

    Can be more than one per student"""
    # Should we figure out how to number these?
    user = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment)
    github_url = models.URLField()
    time_submitted = models.DateTimeField(auto_now_add=True)
    correctness_grade = models.IntegerField(blank=True, null=True)
    style_grade = models.IntegerField(blank=True, null=True)
    graded_by = models.CharField(max_length=30, blank=True)
    note = models.TextField(blank=True)

    def __unicode__(self):
        return "%s by %s" % (self.assignment, self.user)

    @property
    def late(self):
        delta = self.time_submitted - self.assignment.due_date
        if delta > timedelta(0):
            return delta
        else:
            return None
