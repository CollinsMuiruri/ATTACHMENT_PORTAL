from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Student, Course, StudentAttachmentModel
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
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']        
        user.is_student = True
        user.save()
        student = Student.objects.create(
            user=user,
            middle_name=self.cleaned_data['middle_name'],
            email=self.cleaned_data['email'],
            phone_number=self.cleaned_data['phone_number'],
            adm_no=self.cleaned_data['adm_no'],
            course=self.cleaned_data['course'],
            study_mode=self.cleaned_data['study_mode'],
            campus=self.cleaned_data['campus'],
            student_type=self.cleaned_data['student_type'])
        student.save()

        return user



class StudentAttachmentForm(forms.ModelForm):
    date_joined = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = StudentAttachmentModel
        fields = ['stu_name', 'adm_no', 'email', 'phone_number', 'course', 'study_mode',
                  'campus', 'student_type', 'org_name', 'org_location', 'date_joined', 'end_date']
        labels = {
            'stu_name': 'Student Name',
            'adm_no': 'Admission Number',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'course': 'Course',
            'study_mode': 'Study Mode',
            'campus': 'Campus',
            'student_type': 'Student Type',
            'org_name': 'Organization Name',
            'org_location': 'Organization Location',
            'date_joined': 'Date Joined',
            'end_date': 'End Date'
        }
        widgets = {
            'stu_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'adm_no': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'readonly': 'readonly'}),
            'course': forms.TextInput(attrs={'readonly': 'readonly'}),
            'study_mode': forms.TextInput(attrs={'readonly': 'readonly'}),
            'campus': forms.TextInput(attrs={'readonly': 'readonly'}),
            'student_type': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Pop the 'user' from kwargs
        super(StudentAttachmentForm, self).__init__(*args, **kwargs)
        student = self.user.student
        self.fields['stu_name'].initial = student.user.get_full_name()
        self.fields['adm_no'].initial = student.adm_no
        self.fields['email'].initial = student.email
        self.fields['phone_number'].initial = student.phone_number
        self.fields['course'].initial = student.course.name
        self.fields['study_mode'].initial = student.study_mode
        self.fields['campus'].initial = student.campus
        self.fields['student_type'].initial = student.student_type

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.student = self.user.student
        instance.status = True
        if commit:
            instance.save()
        return instance

        
