from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from blog.models import Post

# Import only what exists for now
from blog.models import UserProfile

# We'll import forms individually to avoid errors if some don't exist yet
try:
    from blog.forms import PostForm
except ImportError:
    PostForm = None

try:
    from blog.forms import ProfileForm
except ImportError:
    ProfileForm = None

try:
    from blog.forms import SubscriberForm
except ImportError:
    SubscriberForm = None


def post_full_list(request):
    """View to display all blog posts."""
    # Search functionality
    search_query = request.GET.get("q", "")
    if search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        ).order_by("-created_at")
    else:
        posts = Post.objects.order_by("-created_at")

    # Pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Create button for empty state
    create_button = ""
    if request.user.is_authenticated:
        create_button = f'<a href="{reverse("blog:post_new")}" class="btn btn-primary">Create New Post</a>'

    context = {
        "posts": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "search_query": search_query,
        "create_button": create_button,
    }

    # Use the original template for now until we fix all component issues
    return render(request, "blog/post_list.html", context)


def post_detail(request, pk):
    """View to display a single blog post."""
    post = get_object_or_404(Post, pk=pk)

    # Process markdown content if needed
    import markdown

    try:
        post.rendered_content = markdown.markdown(post.content)
    except:
        post.rendered_content = post.content

    # Find related posts (by tags first, then by date if not enough)
    related_posts = []
    if hasattr(post, "tags") and post.tags.exists():
        # Get posts with similar tags, excluding the current post
        tag_related = (
            Post.objects.filter(tags__in=post.tags.all()).exclude(pk=post.pk).distinct()
        )
        related_posts = list(tag_related[:3])  # Get up to 3 related posts

    # If we don't have enough related posts by tag, add some recent posts
    if len(related_posts) < 3:
        needed = 3 - len(related_posts)
        exclude_ids = [post.pk] + [p.pk for p in related_posts]
        recent_posts = Post.objects.exclude(pk__in=exclude_ids).order_by("-created_at")[
            :needed
        ]
        related_posts.extend(recent_posts)

    context = {"post": post, "related_posts": related_posts}

    # Use the refactored template
    return render(request, "blog/post_detail_refactored.html", context)


def post_new(request):
    """View to create a new blog post."""
    if request.method == "POST" and PostForm:
        # Implementation depends on PostForm existing
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = PostForm() if PostForm else None
    return render(request, "blog/post_edit.html", {"form": form})


def post_edit(request, pk):
    """View to edit an existing blog post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST" and PostForm:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "Post updated successfully!")
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post) if PostForm else None
    return render(request, "blog/post_edit.html", {"form": form, "post": post})


def post_delete(request, pk):
    """View to delete a blog post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect("blog:post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})


def subscribe(request):
    """View for newsletter subscription."""
    context = {}

    if request.method == "POST" and SubscriberForm:
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            messages.success(
                request,
                f"Thank you, {subscriber.name}! You've successfully subscribed to our newsletter.",
            )
            context["success_message"] = (
                f"Thank you, {subscriber.name}! You've successfully subscribed to our newsletter."
            )
        else:
            context["form_errors"] = []
            context["field_errors"] = {}

            for field, errors in form.errors.items():
                if field == "__all__":
                    context["form_errors"].extend(errors)
                else:
                    context["field_errors"][field] = errors

    # Use refactored template
    return render(request, "blog/subscribe_refactored.html", context)


def unsubscribe(request):
    """View for newsletter unsubscription."""
    # Simple placeholder - implementation depends on your subscriber model
    if request.method == "POST" and request.POST.get("email"):
        email = request.POST.get("email")
        # Logic to remove subscriber
        messages.success(request, f"{email} has been unsubscribed from our newsletter.")
        return redirect("blog:main_page")
    return render(request, "blog/unsubscribe.html")


def post_titles_list(request):
    """View to display a list of all blog post titles."""
    posts = Post.objects.order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})


def project_info(request):
    """View to display information about the blog project."""
    context = {
        "fatpy_intro": """
        <p>FatPy is an open-source Python package designed to streamline and standardize fatigue life analysis methods for engineering materials. It aims to provide researchers, engineers, and academics with a robust set of tools for evaluating and predicting fatigue behavior, all within a cohesive and user-friendly framework.</p>
        <p>The package incorporates various fatigue analysis approaches, from traditional stress-life and strain-life methods to more advanced techniques, offering a comprehensive solution for fatigue assessment needs.</p>
        """,
        "contribution_steps": """
        <ol>
            <li><strong>Get to know the project</strong> by exploring the repository and documentation</li>
            <li><strong>Join the discussion</strong> in our GitHub issues and FABER community channels</li>
            <li><strong>Submit pull requests</strong> with bug fixes, improvements, or new features</li>
            <li><strong>Help with documentation</strong> to make FatPy more accessible to new users</li>
        </ol>
        """,
    }
    # Use the refactored template instead of the original
    return render(request, "blog/project_info_refactored.html", context)


def login_view(request):
    """View for user login."""
    # Implementation for login
    return render(request, "blog/login.html")


def logout_view(request):
    """View for user logout."""
    # Implementation for logout
    return redirect("blog:main_page")


def register_view(request):
    """View for user registration."""
    # Implementation for registration
    return render(request, "blog/register.html")


@login_required(login_url="blog:login")
def profile_view(request):
    """View for user profile."""
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == "POST" and ProfileForm:
        form = ProfileForm(request.POST, instance=profile, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("blog:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile, user=user) if ProfileForm else None

    return render(request, "blog/profile.html", {"form": form})
