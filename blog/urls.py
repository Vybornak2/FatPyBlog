from django.urls import path
from blog.views import (
    post_full_list,
    post_detail,
    post_new,
    post_edit,
    post_delete,
    subscribe,
    unsubscribe,
    post_titles_list,
    project_info,
    login_view,
    logout_view,
    register_view,
    profile_view,
)
from blog.views.component_showcase_view import ComponentShowcaseView

app_name = "blog"

urlpatterns = [
    path("", post_full_list, name="main_page"),  # Main page is your post list
    path("posts/", post_full_list, name="post_list"),  # Also have a dedicated posts URL
    path("post/<int:pk>/", post_detail, name="post_detail"),
    path("post/new/", post_new, name="post_new"),
    path("post/<int:pk>/edit/", post_edit, name="post_edit"),
    path("post/<int:pk>/delete/", post_delete, name="post_delete"),
    path("subscribe/", subscribe, name="subscribe"),
    path("unsubscribe/", unsubscribe, name="unsubscribe"),
    path("post/list/", post_titles_list, name="post_titles_list"),
    path("info/", project_info, name="project_info"),
    path("components/", ComponentShowcaseView.as_view(), name="component_showcase"),
    # Authentication URLs
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
]
