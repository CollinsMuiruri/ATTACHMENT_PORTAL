from typing import Any
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from .forms import StudentSignUpForm, LecturerSignUpForm
from django.views.generic import CreateView, ListView
from .models import Student, Lecturer, User, Course
from .forms import UserCreationForm, UserLoginForm
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.contrib import messages
from django.urls import reverse
import json

# Create your views here.
@login_required
def home(request):
    if request.user.is_student:
        student = Student.objects.get(user=request.user)
        print(student.email)
        return render(request, "index.html", {'student':student})
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        return redirect('lec_admin')

@login_required
def lecturer(request):
    if request.user.is_lecturer:
        return render(request, "lecturer/home.html")
    elif request.user.is_student:
        return redirect('home')
    else:
        return redirect('lec_admin')    
    

@login_required
def lec_admin(request):
    if request.user.is_student:
        return render(request, "lecturer/lec_admin.html")
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        return redirect('lec_admin')    
    

@login_required
def apply(request):
    if request.user.is_student:
        return render(request, "apply.html")
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        return redirect('lec_admin')        
    

@login_required
def logbook(request):
    if request.user.is_student:
        return render(request, "logbook.html")
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        return redirect('lec_admin')        
    

@login_required
def downloads(request):
    if request.user.is_student:
        return render(request, "downloads.html")
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        return redirect('lec_admin')        
    


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'auth/stu_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    def form_invalid(self, form):
        # Loop through form errors and display them individually
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)    
    
class LecturerSignUpView(CreateView):
    model = User
    form_class = LecturerSignUpForm
    template_name = 'auth/lec_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'lecturer'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('lecturer')

    def form_invalid(self, form):
        # Loop through form errors and display them individually
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class CoursesListView(ListView):
    model = Course
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses_json"] = json.dumps(list(Course.objects.values()))
        return context
    
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
                    return redirect("/admin")
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
