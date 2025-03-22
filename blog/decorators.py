from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .context_processors import is_editor


def editor_required(view_func):
    """
    Decorator that checks if the user is an editor.
    If not, redirects to the blog list with an error message.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_editor(request.user):
            messages.error(request, "You don't have permission to access this page.")
            return redirect("blog:post_list")
        return view_func(request, *args, **kwargs)

    return wrapper
