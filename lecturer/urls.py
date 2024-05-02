from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path("lecturer", views.lecturer, name="lecturer"),  
    path("lec_admin", views.lec_admin, name="lec_admin"),
    path("auth/register/lecturer/", views.LecturerSignUpView.as_view(), name="lecturer_register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
