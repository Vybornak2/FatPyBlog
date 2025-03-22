"""
Simple script to apply database migrations.
Run this file to update your database schema with the latest migrations.
"""
import os
import sys
import django

if __name__ == "__main__":
    # Setup Django environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FatPyBlog.settings")
    django.setup()

    # Import necessary Django modules
    from django.core.management import call_command
    
    print("Applying database migrations...")
    call_command("migrate")
    print("Migrations applied successfully!")
