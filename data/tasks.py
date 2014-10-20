from celery import task
from celery.exceptions import SoftTimeLimitExceeded
from go_http import HttpApiSender
import rts.settings as settings
import logging
logger = logging.getLogger(__name__)

@task()
def vumi_fire_metric(metric, value, agg, sender=None):
    try:
        if sender is None: 
            sender = HttpApiSender(
                account_key=settings.ACCOUNT_ID,
                conversation_key=settings.CONVERSATION_ID,
                conversation_token=settings.CONVERSATION_TOKEN, 
                api_url=settings.API_URL
            )
        sender.fire_metric(metric, value, agg=agg)
        return sender
    except SoftTimeLimitExceeded:
        logger.error('Soft time limit exceed processing metric fire to Vumi HTTP API via Celery', exc_info=True)
