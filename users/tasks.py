from celery import shared_task
from users.models import User
from datetime import datetime
from django.utils import timezone
from celery.utils.log import get_task_logger
from celery.contrib import rdb
logger = get_task_logger(__name__)
@shared_task
def my_task():
    current_date = timezone.now().date()
    us = User.objects.filter(email = "admin@admin.com").first()
    
    us.access = 'закрыт'
    us.save()
    rdb.set_trace()
    logger.info(us)
    return us