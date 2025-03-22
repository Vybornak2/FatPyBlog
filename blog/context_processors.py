def is_editor(user):
    """Check if a user has editor permissions"""
    return user.is_authenticated and (
        user.is_staff or user.groups.filter(name="Editor").exists()
    )


def editor_context(request):
    """Add editor status to template context"""
    return {"is_editor": is_editor(request.user) if hasattr(request, "user") else False}
