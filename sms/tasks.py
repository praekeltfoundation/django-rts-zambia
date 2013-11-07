from celery.decorators import task
from hierarchy.models import Zone
from sms.sms_sender import VumiGoSender
from django.conf import settings


@task
def send_sms(msisdn, sms):
    sms_vumi = VumiGoSender(api_url=settings.API_URL,
                       account_id=settings.ACCOUNT_ID,
                       conversation_id=settings.CONVERSATION_ID,
                       conversation_token=settings.CONVERSATION_TOKEN)
    sms_vumi.send_sms(msisdn, sms)


@task
def task_query_zone(id, sms):
    school_set = Zone.objects.get(id=id).school_set.all()
    for school in school_set:
        headteacher_set = school.headteacher_set.all()
        for headteacher in headteacher_set:
            send_sms.delay(headteacher.msisdn, sms)
