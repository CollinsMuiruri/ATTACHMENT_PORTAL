from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import StudentSignUpForm
from django.views.generic import CreateView
from .models import Student, User
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your Student views here.
@login_required
def home(request):
    if request.user.is_student:
        student = Student.objects.get(user=request.user)
        print(student.email)
        return render(request, "student/index.html", {'student':student})
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        return redirect('lec_admin')
    
@login_required
def apply(request):
    if request.user.is_student:
        return render(request, "student/apply.html")
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        return redirect('lec_admin')        
    

@login_required
def logbook(request):
    if request.user.is_student:
        return render(request, "student/logbook.html")
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        return redirect('lec_admin')        
    

@login_required
def downloads(request):
    if request.user.is_student:
        return render(request, "student/downloads.html")
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

def test(request)        :
    return render(request, 'test.html')