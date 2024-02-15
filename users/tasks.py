from celery import shared_task
from users.models import User
from datetime import datetime
from django.utils import timezone
from celery.utils.log import get_task_logger
from celery.contrib import rdb
logger = get_task_logger(__name__)
@shared_task
def user_end_date_task():
    current_date = timezone.now().date()
    users = User.objects.filter(end_date__lte = current_date, access='открыт')
    for us in users:
        us.access = 'закрыт'
        us.save()
    # rdb.set_trace()
    # logger.info(us)
    # return us
        

@shared_task
def user_start_date_task():
    current_date = timezone.now().date()
    users = User.objects.filter(start_date__gte = current_date, access='закрыт')
    for us in users:
        us.access = 'открыт'
        us.save()
    # rdb.set_trace()
    # logger.info(us)
    # return us