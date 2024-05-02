from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)


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
    abbreviation = models.CharField(max_length=255)

    def __str__(self):
        return self.name