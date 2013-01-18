from django import forms

from assignments.models import Assignment


class SubmissionForm(forms.Form):
    assignment = forms.ModelChoiceField(
        queryset=Assignment.objects.filter(submissions_open=True),
        empty_label=None)
    github_url = forms.URLField()
