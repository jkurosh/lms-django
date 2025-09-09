import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment variables for Vercel deployment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vetlms.settings')
os.environ.setdefault('USE_SQLITE', 'false')  # Use MySQL on Vercel
os.environ.setdefault('DEBUG', 'False')       # Disable debug on production

# Import Django and get the application
from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIHandler

# Get the Django application
application = get_wsgi_application()

# Vercel requires this variable name
app = application

# Alternative: Create a handler function
def handler(request, context):
    return app(request, context)
