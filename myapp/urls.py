from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("lecturer", views.lecturer, name="lecturer"),
    path("lec_admin", views.lec_admin, name="lec_admin"),
    path("apply/", views.apply, name="apply"),
    path("logbook/", views.logbook, name="logbook"),
    path("downloads/", views.downloads, name="downloads"),
    path("auth/login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("auth/register/student/", views.StudentSignUpView.as_view(), name="student_register"),
    path("auth/register/lecturer/", views.LecturerSignUpView.as_view(), name="lecturer_register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
