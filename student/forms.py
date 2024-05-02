from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Student, Course
from django import forms

from .models import User

SPONSORSHIP = (
    ("SELF", "Self Sponsored Student"),
    ("GOVERNMENT", "Government Sponsored Student"),
)

STUDY_MODE = (
    ("FULL TIME", "Full Time"),
    ("PART TIME", "Part Time"),
    ("DISTANCE LEARNING", "Distance Learning"),
)

CAMPUS = (
    ("MAIN CAMPUS", "Main Campus"),
    ("TOWN CAMPUS", "Town Campus"),
    ("WESTERN CAMPUS", "Western Campus"),
    ("KITENGELA CAMPUS", "Kitengela Campus"),
)


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
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
            # first_name=self.cleaned_data['first_name'],
            # middle_name=self.cleaned_data['middle_name'],
            # last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            phone_number=self.cleaned_data['phone_number'],
            adm_no=self.cleaned_data['adm_no'],
            course=self.cleaned_data['course'],
            study_mode=self.cleaned_data['study_mode'],
            campus=self.cleaned_data['campus'],
            student_type=self.cleaned_data['student_type'])
        student.save()

        return user