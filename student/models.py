from django.db import models
from django.core.exceptions import ValidationError
from myapp.models import User, Course, AttachmentForm
from lecturer.models import Lecturer

# Create your models here.
class Student(models.Model):
    # Sponsorship
    SELF = "Self Sponsored Student"
    GOVERNMENT = "Government Sponsored Student"
    EXTRA = "Extra Sponsored Student"
    SPONSORSHIP = [
        (SELF, "Self Sponsored Student"),
        (GOVERNMENT, "Government Sponsored Student"),
        (EXTRA, "Extra Sponsored Student"),
    ]

    # Study Mode
    FULL = "Full Time"
    PART = "Part Time"
    DISTANCE = "Distance Learning"
    STUDY_MODE = [
        (FULL, "Full Time"),
        (PART, "Part Time"),
        (DISTANCE, "Distance Learning"),
    ]
    
    # Campus
    MAIN = "Main Campus"
    TOWN = "Town Campus"
    WESTERN = "Western Campus"
    KITENGELA = "Kitengela Campus"
    CAMPUS = [
        (MAIN, "Main Campus"),
        (TOWN, "Town Campus"),
        (WESTERN, "Western Campus"),
        (KITENGELA, "Kitengela Campus"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    middle_name = models.CharField(max_length=255, null=True)
    phone_number = models.IntegerField(null=False, default=0000000000)
    email = models.EmailField()
    adm_no = models.CharField(max_length=12)
    course = models.ForeignKey('myapp.Course', on_delete=models.CASCADE, null=False)
    study_mode = models.CharField(max_length=255, choices=STUDY_MODE, default=FULL)
    campus = models.CharField(max_length=255, choices=CAMPUS, default=MAIN)
    student_type = models.CharField(max_length=255, choices=SPONSORSHIP, default=SELF)
    # att_form = models.ForeignKey('myapp.AttachmentForm', on_delete=models.CASCADE, null=True, blank=True)
    # assessor = models.ForeignKey('lecturer.Lecturer', blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username


    def has_submitted_form(self):
        return self.studentattachmentmodel_set.exists()        


class StudentAttachmentModel(models.Model):
    stu_name = models.CharField(max_length=100)
    adm_no = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    study_mode = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    student_type = models.CharField(max_length=100)
    org_name = models.CharField(max_length=100)
    org_location = models.CharField(max_length=100)
    date_joined = models.DateField(max_length=100)
    end_date = models.DateField(max_length=100)
    status = models.BooleanField(default=False)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    assessor = models.ForeignKey('lecturer.Lecturer', blank=True, null=True, on_delete=models.CASCADE)

    
    def save(self, *args, **kwargs):
        if self.student.has_submitted_form():
            # If student has already submitted a form, raise an error
            raise ValidationError("You have already submitted the form.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.student.adm_no} - {self.stu_name} - {self.student.user.username}'