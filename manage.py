#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
<<<<<<< HEAD
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs3240project.settings")
=======
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs3240_project_team2.settings")
>>>>>>> 1bab7e4282aabf671f8e95a56628939cb6204dae

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
