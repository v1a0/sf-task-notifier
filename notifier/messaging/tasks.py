from celery import shared_task


@shared_task()
def add():
    return 45354535345345
