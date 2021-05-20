from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import *
from .models import User


def signup(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        User.objects.create_user(
            request.POST.get('username', ''),
            password=request.POST.get('password1', ''),
            email=request.POST.get('email', '')
        )
        return redirect('/accounts/login')
    return render(request, 'accounts/signup.html', {'form': form, 'title': ('pe-7s-search', 'Register', 'Enter required information.')})


@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'accounts/profile.html', {'user': user})
