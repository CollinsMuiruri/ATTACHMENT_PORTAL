from django.contrib import admin
from .models import User, Course
from student.models import Student, StudentAttachmentModel
from lecturer.models import Lecturer

# Register your models here.
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(User)
admin.site.register(Course)
admin.site.register(StudentAttachmentModel)