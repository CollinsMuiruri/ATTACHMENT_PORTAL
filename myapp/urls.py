from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name="home"),
    # path("test", views.CoursesListView.as_view(), name="test"),
    path("auth/login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
