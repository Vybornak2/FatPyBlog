from django.urls import path
from . import views

app_name = "blog"  # Add this line to define the application namespace

urlpatterns = [
    path("", views.post_full_list, name="post_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/new/", views.post_new, name="post_new"),
    path("post/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("post/<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("unsubscribe/", views.unsubscribe, name="unsubscribe"),
    path("post/list/", views.post_titles_list, name="post_titles_list"),
    # Authentication URLs
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
]
