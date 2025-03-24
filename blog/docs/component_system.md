# FatPyBlog Component System

This document describes the component system used in FatPyBlog.

## Overview

The component system is designed to provide a consistent UI across the application. It consists of:

1. **Template Tags**: Functions that render components
2. **Partial Templates**: HTML templates for individual components
3. **Component CSS**: Styles for each component type
4. **Icon Utilities**: Centralized management of SVG icons

## Available Components

### UI Components

- **Buttons**: `{% render_button url="url" text="Button Text" type="primary" %}`
- **Content Cards**: `{% render_content_card title="Card Title" body="Content here" %}`
- **Tags**: `{% render_tag tag_name="Python" %}`
- **Alerts**: `{% render_alert message="Alert message" type="info" %}`
- **Empty States**: `{% render_empty_state title="No Content" message="No items found" %}`
- **Feature Items**: `{% render_feature_item title="Feature" description="Description" icon_class="bi-star" %}`
- **Link Cards**: `{% render_link_card url="#" text="External Link" icon_class="bi-globe" %}`
- **Post Components**: 
  - `{% render_post_item post %}`
  - `{% render_post_actions post request %}`
  - `{% render_related_posts related_posts %}`
- **Navigation Components**:
  - `{% render_nav_menu request %}`
  - `{% render_account_menu user %}`
  - `{% render_search_form request %}`

### Layout Components

- **Page Headers**: `{% render_page_header title="Page Title" subtitle="Optional subtitle" %}`
- **Page Sections**: `{% render_page_section title="Section Title" body="Content here" %}`
- **Two-Column Layout**: `{% render_two_column_layout main_content="Main" sidebar_content="Sidebar" %}`

### Helper Templates

- **Email Templates**: Base templates for email notifications
- **Pagination**: Helper for rendering consistent pagination

## Usage Guidelines

1. Import the component libraries in your templates:
   ```django
   {% load ui_components %}
   {% load layout_components %}
   ```

2. Use components instead of writing HTML directly:
   ```django
   {% render_button url="blog:post_new" text="Create Post" type="primary" icon="bi-plus" %}
   ```

3. For icons, use Bootstrap icon classes (e.g., `bi-plus`, `bi-house`).

4. For complex pages, combine layout components:
   ```django
   {% render_page_header title="Dashboard" %}
   {% render_page_section title="Statistics" body=stats_html %}
   ```

## Component Showcase

The component showcase page at `/components/` displays all available components with usage examples. Use this as a reference when building new pages.
