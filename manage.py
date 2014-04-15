#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Add src to the PYTHON_PATH
    ROOT = os.path.dirname(__file__)
    PATH = os.path.abspath(os.path.join(ROOT, 'src'))
    if PATH not in sys.path:
        sys.path.insert(0, PATH)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kawaz.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
