import os
from django.core.management import call_command

# Set DJANGO_SETTINGS_MODULE to point to your settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicsource.settings')

# Dump the data
with open("db_backup.json", "w", encoding="utf-8") as buffer:
    call_command("dumpdata", indent=2, stdout=buffer)
