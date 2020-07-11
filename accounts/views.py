from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegistrationForm

# Create your views here.
@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, "Thanks for visiting, see you again soon!")
    return redirect(reverse('index'))


def index(request):
    if request.user.is_authenticated:
        print(request.user)
    if request.method == "POST":
        if request.POST.get('submit') == 'sign_in':
            form = UserLoginForm(request.POST)

            if form.is_valid():
                user = auth.authenticate(username=request.POST['username'],
                                        password=request.POST['password'])

                if user:
                    auth.login(user=user, request=request)
                    messages.success(request, "Welcome, " + user.first_name + "!")
                    return redirect(reverse('watchlist:watchlist'))
                else:
                    form.add_error(None, "Your username or password is incorrect.")
        elif request.POST.get('submit') == 'sign_up':
            registration_form = UserRegistrationForm(request.POST)
            if registration_form.is_valid():
                registration_form.save()

                user = auth.authenticate(username=request.POST['username'],
                                        password=request.POST['password1'])
                if user:
                    auth.login(user=user, request=request)
                    messages.success(request, "Welcome, " + user.first_name +
                                    "! Your account was successfully created.")
                    return redirect(reverse('watchlist:watchlist'))
                else:
                    registration_form.add_error(
                        request("Sorry, we are unable to register your account at this time."))
    context = {
        "login_form": UserLoginForm,
        "registration_form": UserRegistrationForm
    }
    return render(request, "index.html", context)