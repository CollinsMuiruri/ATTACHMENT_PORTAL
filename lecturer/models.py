from django.db import models
from myapp.models import User, Course


# Create your models here.
class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    lec_id = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=False)
    courses = models.ManyToManyField('myapp.Course')
    assessor_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
