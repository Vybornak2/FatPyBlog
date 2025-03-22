# FatPyWeb

A Django web application.

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Project Structure

- `FatPyWeb/` - Main project directory
  - `settings/` - Settings modules
  - `static/` - Project static files
  - `templates/` - Project templates
- `apps/` - Application modules
- `staticfiles/` - Collected static files

## Development Guidelines

- Follow PEP 8 style guide
- Write unit tests for new functionality
- Update requirements.txt when adding new dependencies
