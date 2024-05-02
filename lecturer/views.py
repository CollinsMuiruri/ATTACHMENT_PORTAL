from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import LecturerSignUpForm
from django.contrib import messages
from myapp.models import User
from .models import Lecturer


# Create your views here.
@login_required
def lecturer(request):
    if request.user.is_lecturer:
        lec = Lecturer.objects.get(user=request.user)
        print(lec)

        return render(request, "lecturer/home.html", {"lec":lec})
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
