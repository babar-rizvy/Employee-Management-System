#!/usr/bin/env python
import os
import sys
from importlib import import_module

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    execute_from_command_line = import_module("django.core.management").execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
