from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # Post views
    path("", views.PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    # Category views
    path(
        "category/<slug:slug>/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    # Admin views
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path(
        "post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"
    ),
]
