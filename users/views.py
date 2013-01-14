from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def user_home(request):
    return render(request, 'users/user_home.html')
