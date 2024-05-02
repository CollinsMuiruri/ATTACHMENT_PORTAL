from typing import Any
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, ListView
from .forms import UserCreationForm, UserLoginForm
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.contrib import messages
from .models import User, Course
from django.urls import reverse
import json

# Create your Myapp views here.
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
