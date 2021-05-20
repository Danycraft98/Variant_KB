# !/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # os.system('python manage.py makemigrations')
    # os.system('python manage.py migrate')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "variant-kb.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    execute_from_command_line(sys.argv)
