from celery.decorators import task
from hierarchy.models import Zone
from sms.sms_sender import VumiGoSender


@task
def send_sms(msisdn, sms):
    sms = VumiGoSender(api_url="",
                       account_id="",
                       conversation_id="",
                       conversation_token="")

    sms.send_sms(msisdn, sms)


@task
def task_query_zone(id, sms):
    school_set = Zone.objects.get(id=id).school_set.all()

    for school in school_set:
        headteacher_set = school.headteacher_set.all()
        for headteacher in headteacher_set:
            send_sms.delay(headteacher.msisdn, sms)
