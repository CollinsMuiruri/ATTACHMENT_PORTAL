from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Lecturer
from django import forms
from myapp.models import Course, User


# Boolean choices for assessor
BOOLEAN_CHOICES = (
    (True, 'Available'),
    (False, 'Not Available'),
)

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
