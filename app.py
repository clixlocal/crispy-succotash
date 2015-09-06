from datetime import datetime
import os, pdb
# from apscheduler.schedulers.blocking import BlockingScheduler


def run_job():
  date = datetime.now()
  sub_folder = str(date.hour)

  s3_folder = '{0}-{1}-{2}/{3}/'.format(str(date.year), str(date.month), str(date.day), sub_folder)

  os.system('python -m scripts.radian6 --hours {0} {1}'.format('12', s3_folder))
  # TODO: Add this in whenever post_prepper is reading from s3
  # os.system('python -m scripts.post_prepper {0}'.format(s3_folder))

# sched = BlockingScheduler()
# sched.add_job(run_job, 'cron', hour=8)
# sched.add_job(run_job, 'cron', hour=16)
# sched.start()

run_job()

