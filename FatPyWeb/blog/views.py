from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Subscription
from .forms import PostForm, SubscriptionForm
import markdown


def post_list(request):
    query = request.GET.get("q")
    if query:
        posts = Post.objects.filter(title__icontains=query).order_by("-created_at")
    else:
        posts = Post.objects.all().order_by("-created_at")
    for post in posts:
        post.content = markdown.markdown(post.content)
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.content = markdown.markdown(post.content)
    return render(request, "blog/post_detail.html", {"post": post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})


def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect with success parameter
            return redirect("subscribe?subscribed=true")
    else:
        form = SubscriptionForm()
    return render(request, "blog/subscribe.html", {"form": form})
