from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Post, Subscription
from .forms import PostForm, SubscriptionForm
import markdown
import re


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


def post_list(request):
    query = request.GET.get("q")
    if query:
        posts = Post.objects.filter(title__icontains=query).order_by("-created_at")
    else:
        posts = Post.objects.all().order_by("-created_at")

    # Convert markdown to HTML for each post
    posts = [prepare_post_for_display(post) for post in posts]

    context = {
        "posts": posts,
        "query": query,
        "no_results": query and not posts,
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post = prepare_post_for_display(post)
    return render(request, "blog/post_detail.html", {"post": post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect("blog:post_detail", pk=post.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "Post updated successfully!")
            return redirect("blog:post_detail", pk=post.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})


def post_delete(request, pk):
    """Delete a post."""
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect("blog:post_list")

    return render(request, "blog/post_delete.html", {"post": post})


def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing!")
            return redirect(f"{reverse('blog:subscribe')}?subscribed=true")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SubscriptionForm()
    return render(request, "blog/subscribe.html", {"form": form})
