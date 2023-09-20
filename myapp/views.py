from typing import Any
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from .forms import StudentSignUpForm, LecturerSignUpForm
from .forms import UserCreationForm, UserLoginForm
from .models import Student, Lecturer, User
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib import messages

# Create your views here.
@login_required
def home(request):
    if request.user.is_student:
        return render(request, "index.html")
    else:
        return redirect('lecturer')

def lecturer(request):
    return render(request, "lecturer/home.html")

def apply(request):
    return render(request, "apply.html")


def logbook(request):
    return render(request, "logbook.html")


def downloads(request):
    return render(request, "downloads.html")


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'auth/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
class LecturerSignUpView(CreateView):
    model = User
    form_class = LecturerSignUpForm
    template_name = 'auth/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'lecturer'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('lecturer')
    

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
                    return redirect("admin")
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
