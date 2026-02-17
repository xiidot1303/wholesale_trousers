from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from django_apscheduler.jobstores import register_events, DjangoJobStore
from app.scheduled_job import report_job

# Configure executors and sensible job defaults for production
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5),
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1,
    'misfire_grace_time': 300,  # seconds
}

class jobs:
    scheduler = BlockingScheduler(timezone='Asia/Tashkent', executors=executors, job_defaults=job_defaults)
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    scheduler.add_job(report_job.create_daily_product_balance, 'cron',
                      hour=23, minute=40, id='create_daily_product_balance')
