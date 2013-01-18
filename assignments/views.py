from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from github_api.models import Github
from assignments.forms import SubmissionForm
from assignments.models import Submission, Assignment


@login_required
def submit(request):
    error_message = None
    submission = None
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            gh = Github.objects.get()
            url = request.POST['github_url']
            gh.acknowledge_pull(request.user, url)

            assignment = Assignment.objects.get(id=request.POST['assignment'])
            submission = Submission(user=request.user, assignment=assignment,
                                    github_url=url)
            submission.save()
            success = True
        else:
            pass
    else:
        form = SubmissionForm()

    return render(request, "assignments/submit.html", {
        'form': form,
        'error_message': error_message,
        'submission': submission,
    })
