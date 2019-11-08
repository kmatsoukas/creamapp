from celery.schedules import crontab
from celery.task import periodic_task
from client.models import Subscription


@periodic_task(run_every=crontab(minute=0, hour=9))
def schedule():
    days_to_fetch = [14, 7, 2, 1]
    # get all the notifications that expire in 7, 2, 1 days
    for days in days_to_fetch:
        # query the database for any expiring subscriptions
        qset = Subscription.expire_in_days(days)
        if qset:
            for sub in qset:
                sub.notify_expiration(days)