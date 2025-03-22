from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("profile/", views.ProfileDetailView.as_view(), name="profile-detail"),
    path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile-edit"),
]
