from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)


class Student(models.Model):
    SELF = "SSS"
    GOVERNMENT = "GSS"
    SPONSORSHIP = [
        (SELF, "SSS"),
        (GOVERNMENT, "GSS"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    middle_name = models.CharField(max_length=255, null=True)
    phone_number = models.IntegerField(null=False, default=0000000000)
    adm_no = models.CharField(max_length=12)
    course = models.CharField(max_length=255)
    study_mode = models.CharField(max_length=255)
    campus = models.CharField(max_length=255)
    student_type = models.CharField(max_length=3, choices=SPONSORSHIP, default=SELF)

    def __str__(self):
        return self.user.username


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    lec_id = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
