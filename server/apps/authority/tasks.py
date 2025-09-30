import os
from celery import shared_task
from django.core.management import call_command


@shared_task
def sync_authority_from_seed() -> str:
    path = os.getenv("AUTHORITY_SEED_PATH", "data/ics/2023")
    call_command("load_authority", path)
    return f"loaded:{path}"

