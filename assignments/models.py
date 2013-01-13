from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Assignment(models.Model):
    due_date = models.DateTimeField("due date")
    name = models.CharField(max_length=80)
    url = models.URLField("website", blank=True)

    def __unicode__(self):
        return "Assignment '%(name)s'" % self.__dict__


class Submission(models.Model):
    user = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment)
    url = models.URLField("Github URL", blank=True)
    time_submitted = models.DateTimeField("time submitted", auto_now_add=True)
    correctness_grade = models.IntegerField("correctness grade")
    style_grade = models.IntegerField()

    def __unicode__(self):
        return "%s by %s" % (self.assignment, self.user)
