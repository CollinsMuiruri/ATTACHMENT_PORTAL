from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("apply/", views.apply, name='apply'),
    path("logbook/", views.logbook, name='logbook'),
    path("downloads/", views.downloads, name='downloads'),
    path("auth/login/", views.login, name='login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)