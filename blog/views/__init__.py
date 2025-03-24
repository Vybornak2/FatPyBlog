# Import views from other view modules
from blog.views.views import (
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

# Make them available directly from blog.views
__all__ = [
    "post_full_list",
    "post_detail",
    "post_new",
    "post_edit",
    "post_delete",
    "subscribe",
    "unsubscribe",
    "post_titles_list",
    "project_info",
    "login_view",
    "logout_view",
    "register_view",
    "profile_view",
]
