from datetime import datetime
import os

date = datetime.utcnow()
if date.hour > 12:
  sub_folder = 'afternoon'
else:
  sub_folder = 'morning'

s3_folder = '{0}-{1}-{2}/{3}/'.format(str(date.year), str(date.month), str(date.day), sub_folder)

os.system('python -m scripts.radian6 {0}'.format(s3_folder))
