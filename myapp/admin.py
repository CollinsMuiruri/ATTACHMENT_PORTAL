from django.contrib import admin
from .models import Student, Lecturer, User

# Register your models here.
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(User)