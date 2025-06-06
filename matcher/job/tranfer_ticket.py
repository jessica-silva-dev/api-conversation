from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from matcher.views import TransferTicketAgent
from django.conf import settings


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

executors = {
    'default': ThreadPoolExecutor(3)
}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    timezone=settings.TIME_ZONE
)

transfer_agent = TransferTicketAgent()

scheduler.add_job(
    func=transfer_agent.transfer_agents_online,
    trigger='interval',
    minutes=1,
)   