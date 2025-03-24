from django.views.generic import TemplateView
from django.core.paginator import Paginator
from blog.models import Post


class ComponentShowcaseView(TemplateView):
    """View to showcase available UI components"""

    template_name = "blog/component_showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_subtitle"] = "Component Library"

        # Add sample post if available
        try:
            sample_post = Post.objects.order_by("-created_at").first()
            context["sample_post"] = sample_post
        except:
            context["sample_post"] = None

        # Add related posts if available
        try:
            related_posts = Post.objects.order_by("-created_at")[:3]
            if related_posts:
                context["related_posts"] = related_posts
        except:
            pass

        # Create a dummy paginator for demonstration
        try:
            # Use actual posts if available
            all_posts = Post.objects.all()
            if all_posts.exists():
                paginator = Paginator(all_posts, 10)
                page_obj = paginator.get_page(1)
                context["page_obj"] = page_obj
        except:
            pass

        return context
