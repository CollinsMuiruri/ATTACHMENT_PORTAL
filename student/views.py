from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import StudentSignUpForm, StudentAttachmentForm
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from .models import Student, User, StudentAttachmentModel
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your Student views here.
@login_required
def home(request):
    if request.user.is_student:
        student = Student.objects.get(user=request.user)
        print(student.email)
        att_form = StudentAttachmentModel.objects.filter(student=student).first()
        return render(request, "student/index.html", {'student':student, 'att_form':att_form})
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        return redirect('admin/')
    
# @login_required
# def apply(request):
#     if request.user.is_student:
#         if request.method =='POST':
#             form = StudentAttachmentForm(request, data=request.POST)
#             if form.is_valid():
#                 form.status = True
#                 form.save()
#                 return render(request, "student/index.html", {'form':form})
#             else:
#                 messages.error(request, "invalid Details.")
#         form = StudentAttachmentForm()
#         # print(form.stu_name)
#         return render(request, "student/apply.html", {'form':form})
#     elif request.user.is_lecturer:
#         return redirect('lecturer')
#     else:
#         # return redirect('lec_admin') Will late Make a view for an admin to view the pages as an admin
#         return redirect('admin/')      
    
class ApplyFormView(LoginRequiredMixin, FormView):
    template_name = 'student/apply.html'
    form_class = StudentAttachmentForm
    success_url = "/home/"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Form submitted successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Loop through form errors and display them individually
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the logged-in user to the form
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.user.student.has_submitted_form():
            messages.error(self.request, 'You have already submitted the form.')
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)
    

@login_required
def logbook(request):
    if request.user.is_student:
        return render(request, "student/logbook.html")
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        # return redirect('lec_admin') Will late Make a view for an admin to view the pages as an admin
        return redirect('admin/')      
        
    

@login_required
def downloads(request):
    if request.user.is_student:
        return render(request, "student/downloads.html")
    elif request.user.is_lecturer:
        return redirect('lecturer')
    else:
        # return redirect('lec_admin') Will late Make a view for an admin to view the pages as an admin
        return redirect('admin/')      
        
            

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

@login_required
def attachment_signup(request):
    if request.method == 'POST':
        form = StudentAttachmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentAttachmentForm()

    return render(request, 'student/apply.html', {})
        

def track_attachment_progress(request):
    # set a status_color variable, if status is not done, grey; in progress: yellow; done: green - use in-file styles for this
    # if attachment_form,status = True,
    # add 10% to percentage
    # if logbook progress is set to started,
    # add 10% to percentage
    # if logbook progress is set to ongoing,
    # add 10% to percentage
    # if logbook progress is set to completed,
    # add 10% to percentage
    pass

def track_logbook_progress(request):
    # You could also instead use a specified number of weeks per course
    # Based on the submitted form, use the date of joining for proper tracking of weeks
    # For each day, check if form was submitted
    # Change form status and have a date + time stamp stored when done
    # You cannot input a log before the previous one is done
    # if all 5days in the week are filled, mark the week as done, turn to green
    pass


def test(request):
    return render(request, 'test.html')