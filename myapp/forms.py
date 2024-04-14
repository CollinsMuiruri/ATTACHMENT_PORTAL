from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Student, Lecturer, Course
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

# Boolean choices for assessor
BOOLEAN_CHOICES = (
    (True, 'Available'),
    (False, 'Not Available'),
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
            first_name=self.cleaned_data['first_name'],
            middle_name=self.cleaned_data['middle_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            phone_number=self.cleaned_data['phone_number'],
            adm_no=self.cleaned_data['adm_no'],
            course=self.cleaned_data['course'],
            study_mode=self.cleaned_data['study_mode'],
            campus=self.cleaned_data['campus'],
            student_type=self.cleaned_data['student_type'])
        student.save()

        return user

# Custom class to help in selcting both the name and the abbreviation of the course
class CustomCourseChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} ({obj.abbreviation})"        
    
class LecturerSignUpForm(UserCreationForm):
    lec_id = forms.CharField(required=True)
    phone_number = forms.CharField(max_length=255, required=True)
    # courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), required=True)
    courses = CustomCourseChoiceField(queryset=Course.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'select2'}))
    assessor_status = forms.ChoiceField(choices=BOOLEAN_CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['courses'].widget.attrs['size'] = len(self.fields['courses'].queryset)
            
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username', 
            'first_name', 
            'last_name', 
            'lec_id', 
            'email',
            'phone_number',
            'assessor_status',
            'courses'
            )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.save()
        lecturer = Lecturer.objects.create(
            user=user,
            lec_id=self.cleaned_data['lec_id'],
            phone_number=self.cleaned_data['phone_number'],
            assessor_status=self.cleaned_data['assessor_status'],
            )
        lecturer.courses.set(self.cleaned_data['courses']),
        
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