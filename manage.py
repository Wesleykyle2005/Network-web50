"""Archivo de gestión para Django."""

import os
import sys


def main():
    """Punto de entrada para la gestión de Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project4.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
