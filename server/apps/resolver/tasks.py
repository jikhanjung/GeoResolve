from celery import shared_task


@shared_task
def echo(text: str) -> str:
    return text

