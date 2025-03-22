from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import os


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category_detail", kwargs={"slug": self.slug})


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique_for_date="publish")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()
    featured_image = models.ImageField(
        upload_to="blog/featured_images/", blank=True, null=True
    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ["-publish"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # Ensure the upload_to directory exists
        if self.featured_image:
            directory = os.path.dirname(self.featured_image.path)
            if not os.path.exists(directory):
                os.makedirs(directory)

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            kwargs={
                "year": self.publish.year,
                "month": self.publish.month,
                "day": self.publish.day,
                "slug": self.slug,
            },
        )
