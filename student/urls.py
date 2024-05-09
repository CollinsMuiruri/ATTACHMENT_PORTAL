from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("test/", views.test, name="test"),
    # path("apply/", views.apply, name="apply"),
    path("apply/", views.ApplyFormView.as_view(), name="apply"),
    path("logbook/", views.logbook, name="logbook"),
    path("downloads/", views.downloads, name="downloads"),
    path("auth/register/student/", views.StudentSignUpView.as_view(), name="student_register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
