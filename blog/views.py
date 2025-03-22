from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.conf import settings  # Add this import to fix the NameError
from .models import Post, Subscription, UserProfile, Tag
from .forms import PostForm, SubscriptionForm, LoginForm, RegisterForm, ProfileForm
import markdown
import re
from .decorators import editor_required
from .email_utils import send_welcome_email
import logging

logger = logging.getLogger(__name__)


def process_markdown_content(content):
    """Process markdown content with enhanced image handling"""
    # First convert with standard extensions
    html_content = markdown.markdown(
        content, extensions=["fenced_code", "tables", "nl2br"]
    )

    # Post-process to ensure images have proper classes and attributes
    # Find all image tags and add the md-image-override class
    pattern = re.compile(r"<img([^>]*)>")

    def add_class_to_img(match):
        attributes = match.group(1)
        if "class=" in attributes:
            # Add the class to existing classes
            attributes = re.sub(
                r'class=(["\'])(.*?)(["\'])',
                r"class=\1\2 md-image-override\3",
                attributes,
            )
        else:
            # Add the class attribute
            attributes += ' class="md-image-override"'

        # Remove any width or height attributes
        attributes = re.sub(r'width=(["\'])(.*?)(["\'])', "", attributes)
        attributes = re.sub(r'height=(["\'])(.*?)(["\'])', "", attributes)
        attributes = re.sub(r'style=(["\'])(.*?)(["\'])', "", attributes)

        return f"<img{attributes}>"

    html_content = re.sub(pattern, add_class_to_img, html_content)

    return html_content


def prepare_post_for_display(post):
    """Prepare a post object for display by processing its markdown content"""
    post.content = process_markdown_content(post.content)
    return post


def post_full_list(request):
    """View to display all posts with full content (main page)."""
    query = request.GET.get("q")
    if query:
        # Modified search to exclude content, only search title, author and tags
        posts = (
            Post.objects.filter(
                Q(title__icontains=query)
                | Q(author__username__icontains=query)
                | Q(author__first_name__icontains=query)
                | Q(author__last_name__icontains=query)
                | Q(tags__name__icontains=query)  # Fixed: changed () to =
            )
            .distinct()
            .order_by("-created_at")
        )
    else:
        posts = Post.objects.all().order_by("-created_at")

    # Convert markdown to HTML for each post
    posts = [prepare_post_for_display(post) for post in posts]

    context = {
        "posts": posts,
        "query": query,
        "no_results": query and not posts,
    }
    return render(request, "blog/main_page.html", context)


def post_titles_list(request):
    """View to display a list of all posts titles and dates only."""
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post = prepare_post_for_display(post)
    return render(request, "blog/post_detail.html", {"post": post})


@editor_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post created successfully!")
            return redirect("blog:post_detail", pk=post.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PostForm(user=request.user)

    # Render the form content separately
    form_content = render(
        request, "blog/partials/_form_content.html", {"form": form}
    ).content.decode("utf-8")

    return render(
        request, "blog/post_edit.html", {"form": form, "form_content": form_content}
    )


@editor_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Check if the user is the author of the post
    if post.author and post.author != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect("blog:post_detail", pk=post.pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post, user=request.user)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post updated successfully!")
            return redirect("blog:post_detail", pk=post.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PostForm(instance=post, user=request.user)

    # Render the form content separately
    form_content = render(
        request, "blog/partials/_form_content.html", {"form": form}
    ).content.decode("utf-8")

    return render(
        request, "blog/post_edit.html", {"form": form, "form_content": form_content}
    )


@editor_required
def post_delete(request, pk):
    """Delete a post."""
    post = get_object_or_404(Post, pk=pk)

    # Check if the user is the author of the post
    if post.author and post.author != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to delete this post.")
        return redirect("blog:post_detail", pk=post.pk)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect("blog:post_list")

    # Render the delete content separately
    delete_content = render(
        request, "blog/partials/_delete_content.html", {"post": post}
    ).content.decode("utf-8")

    return render(
        request,
        "blog/post_delete.html",
        {"post": post, "delete_content": delete_content},
    )


def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save()

            email_message = "Thank you for subscribing!"
            if settings.ENABLE_EMAIL_NOTIFICATIONS:
                if settings.EMAIL_BACKEND.endswith("console.EmailBackend"):
                    email_message += (
                        " A welcome email has been sent (check your console output)."
                    )
                elif settings.EMAIL_BACKEND.endswith("filebased.EmailBackend"):
                    email_message += f" A welcome email has been saved to {settings.EMAIL_FILE_PATH}."
                else:
                    email_message += (
                        " A welcome email has been sent to your email address."
                    )

                try:
                    send_welcome_email(subscription.email)
                    logger.info(f"Welcome email sent to {subscription.email}")
                except Exception as e:
                    logger.error(f"Failed to send welcome email: {str(e)}")

            messages.success(request, email_message)
            return redirect(f"{reverse('blog:subscribe')}?subscribed=true")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SubscriptionForm()
    return render(request, "blog/subscribe.html", {"form": form})


def unsubscribe(request):
    # Get email from either query params or POST data
    email = request.GET.get("email") or ""

    if request.method == "POST":
        email = request.POST.get("email")
        try:
            subscription = Subscription.objects.get(email=email)
            subscription.delete()
            messages.success(request, "You have been unsubscribed successfully.")
            return redirect("blog:post_list")
        except Subscription.DoesNotExist:
            messages.error(request, "This email is not in our subscription list.")

    return render(request, "blog/unsubscribe.html", {"email": email})


# Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect("blog:post_list")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the page the user was trying to access or default to home
                next_page = request.GET.get("next", "blog:post_list")
                return redirect(next_page)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "blog/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("blog:post_list")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("blog:post_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Explicitly create UserProfile after user is saved
            try:
                # Check if profile was automatically created by signals
                profile = UserProfile.objects.filter(user=user).first()
                if not profile:
                    profile = UserProfile.objects.create(
                        user=user,
                        title=form.cleaned_data.get("title", ""),
                        name=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
                    )

                # Handle newsletter subscription
                if form.cleaned_data.get("subscribe"):
                    email = form.cleaned_data.get("email")
                    if not Subscription.objects.filter(email=email).exists():
                        Subscription.objects.create(email=email)

            except Exception as e:
                # Log the error but continue (the user is still created)
                print(f"Error creating user profile: {e}")

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("blog:post_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "blog/register.html", {"form": form})


@login_required(login_url="blog:login")
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("blog:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile, user=user)

    return render(request, "blog/profile.html", {"form": form})
