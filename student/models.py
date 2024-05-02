from django.db import models
from myapp.models import User, Course, AttachmentForm
from lecturer.models import Lecturer

# Create your models here.
class Student(models.Model):
    # Sponsorship
    SELF = "Self Sponsored Student"
    GOVERNMENT = "Government Sponsored Student"
    SPONSORSHIP = [
        (SELF, "Self Sponsored Student"),
        (GOVERNMENT, "Government Sponsored Student"),
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
    att_form = models.ForeignKey('myapp.AttachmentForm', on_delete=models.CASCADE, null=True, blank=True)
    assessor = models.ForeignKey('lecturer.Lecturer', blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username
