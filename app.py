from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler


def run_job():
  date = datetime.utcnow()
  if date.hour > 12:
    sub_folder = 'afternoon'
  else:
    sub_folder = 'morning'

  s3_folder = '{0}-{1}-{2}/{3}/'.format(str(date.year), str(date.month), str(date.day), sub_folder)

  os.system('python -m scripts.radian6 {0} {1}'.format('12', s3_folder))
  os.system('python -m scripts.post_prepper {0}'.format(s3_folder))

# sched = BlockingScheduler()
# sched.add_job(run_job, 'cron', hour=8)
# sched.add_job(run_job, 'cron', hour=20)
# sched.start()

run_job()

