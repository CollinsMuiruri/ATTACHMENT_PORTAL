from django.contrib import messages
from .models import User
from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
@login_required
def home(request):
    return render(request, "index.html")


def apply(request):
    return render(request, "apply.html")


def logbook(request):
    return render(request, "logbook.html")


def downloads(request):
    return render(request, "downloads.html")


# @login_required
def register_request(request):
    # if not User.Role == "ADMIN":
    #     return redirect("auth/login/?next=/auth/register/")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserCreationForm()
    return render(
        request=request,
        template_name="auth/register.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if user.is_student:
                    return redirect("home")
                elif user.is_lecturer:
                    return redirect("lecturer")
                else:
                    return redirect("admin/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = UserLoginForm()
    return render(
        request=request, template_name="auth/login.html", context={"login_form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")
