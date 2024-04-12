from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)


class Student(models.Model):
    # Sponsorship
    SELF = "SSS"
    GOVERNMENT = "GSS"
    SPONSORSHIP = [
        (SELF, "SSS"),
        (GOVERNMENT, "GSS"),
    ]

    # Study Mode
    FULL = "FULL TIME"
    PART = "PART TIME"
    DISTANCE = "DISTANCE LEARNING"
    STUDY_MODE = [
        (FULL, "FULL TIME"),
        (PART, "PART TIME"),
        (DISTANCE, "DISTANCE LEARNING"),
    ]
    
    # Campus
    MAIN = "MAIN CAMPUS"
    TOWN = "TOWN CAMPUS"
    WESTERN = "WESTERN CAMPUS"
    KITENGELA = "KITENGELA CAMPUS"
    CAMPUS = [
        (MAIN, "MAIN CAMPUS"),
        (TOWN, "TOWN CAMPUS"),
        (WESTERN, "WESTERN CAMPUS"),
        (KITENGELA, "KITENGELA CAMPUS"),
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    middle_name = models.CharField(max_length=255, null=True)
    phone_number = models.IntegerField(null=False, default=0000000000)
    adm_no = models.CharField(max_length=12)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=False)
    study_mode = models.CharField(max_length=255, choices=STUDY_MODE, default=FULL)
    campus = models.CharField(max_length=255, choices=CAMPUS, default=MAIN)
    student_type = models.CharField(max_length=3, choices=SPONSORSHIP, default=SELF)
    att_form = models.ForeignKey('AttachmentForm', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    lec_id = models.CharField(max_length=255)
    courses = models.ManyToManyField('Course')

    def __str__(self):
        return self.user.username

class AttachmentForm(models.Model):
    status = models.BooleanField(default=False)
    organisation = models.CharField(max_length=255)
    join_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        if self.status == True:
            return 'Submitted'
        else:
            return 'Not Submitted'
        
class Course(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name