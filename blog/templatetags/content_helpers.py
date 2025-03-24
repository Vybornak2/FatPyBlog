from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def as_html_content(text):
    """Convert text to HTML content by wrapping paragraphs"""
    if not text:
        return ""

    paragraphs = text.strip().split("\n\n")
    html = "".join([f"<p>{p}</p>" for p in paragraphs if p.strip()])
    return mark_safe(html)


@register.simple_tag
def render_pagination(page_obj, url_param="page"):
    """Render pagination controls

    Args:
        page_obj: Django pagination object
        url_param: URL parameter name for page
    """
    if not page_obj.paginator.num_pages > 1:
        return ""

    html = ['<div class="pagination">']
    html.append('<span class="step-links">')

    if page_obj.has_previous():
        html.append(f'<a href="?{url_param}=1">&laquo; first</a>')
        html.append(
            f'<a href="?{url_param}={page_obj.previous_page_number()}">previous</a>'
        )

    html.append(
        f'<span class="current">Page {page_obj.number} of {page_obj.paginator.num_pages}</span>'
    )

    if page_obj.has_next():
        html.append(f'<a href="?{url_param}={page_obj.next_page_number()}">next</a>')
        html.append(
            f'<a href="?{url_param}={page_obj.paginator.num_pages}">last &raquo;</a>'
        )

    html.append("</span>")
    html.append("</div>")

    return mark_safe("".join(html))
