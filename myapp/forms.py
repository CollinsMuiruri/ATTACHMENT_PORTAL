from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Student, Lecturer, Course
from django import forms

from .models import User

SPONSORSHIP = (
    ("SELF", "SSS"),
    ("GOVERNMENT", "GSS"),
)

STUDY_MODE = (
    ("FULL TIME", "FULL TIME"),
    ("PART TIME", "PART TIME"),
    ("DISTANCE LEARNING", "DISTANCE LEARNING"),
)

CAMPUS = (
    ("MAIN CAMPUS", "MAIN CAMPUS"),
    ("TOWN CAMPUS", "TOWN CAMPUS"),
    ("WESTERN CAMPUS", "WESTERN CAMPUS"),
    ("KITENGELA CAMPUS", "KITENGELA CAMPUS"),
)

class StudentSignUpForm(UserCreationForm):
    middle_name = forms.CharField(required=True)
    phone_number = forms.IntegerField(required=True)
    adm_no = forms.CharField(required=True)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)
    study_mode = forms.ChoiceField(choices=STUDY_MODE, required=True)
    campus = forms.ChoiceField(choices=CAMPUS, required=True)
    student_type = forms.ChoiceField(choices=SPONSORSHIP, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "adm_no",
            "course",
            "study_mode",
            "campus",
            "student_type",
        )
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(
            user=user,
            middle_name=self.cleaned_data['middle_name'],
            phone_number=self.cleaned_data['phone_number'],
            adm_no=self.cleaned_data['adm_no'],
            course=self.cleaned_data['course'],
            study_mode=self.cleaned_data['study_mode'],
            campus=self.cleaned_data['campus'],
            student_type=self.cleaned_data['student_type'])
        student.save()

        return user
    
class LecturerSignUpForm(UserCreationForm):
    lec_id = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'lec_id')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.save()
        lecturer = Lecturer.objects.create(user=user, lec_id=self.cleaned_data['lec_id'])
        lecturer.save()

        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(attrs={"placeholder": "1234567", "required": True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "• • • • • • • • • • • • • • •",
                "id": "password-input",
            }
        )
    )