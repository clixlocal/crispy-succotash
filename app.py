from datetime import datetime
import os, pdb, subprocess, gmail, json


def run_job():
  date = datetime.now()
  sub_folder = str(date.hour)

  s3_folder = '{0}-{1}-{2}/{3}/'.format(str(date.year), str(date.month), str(date.day), sub_folder)
  email_config = json.load(open('config/email.json'))
  account = gmail.GMail(email_config['sender_email'], email_config['sender_pass'])

  hours_to_pull = '24'

  try:
    os.system('python -m scripts.radian6 --hours {0} {1}'.format(hours_to_pull, s3_folder))
    result = subprocess.Popen(['python', '-m', 'scripts.post_prepper', '{0}'.format(s3_folder)], stdout=subprocess.PIPE).stdout.read()
    email_message = ('''
    The Radian6 to Salesforce export/import ran with the following results:

    {0}
    ''').format(result)
    msg = gmail.Message('Radian6 to Salesforce results',
                        to=', '.join(email_config['recipients']),
                        text=email_message)
    account.send(msg)
    print(result)
  except:
    e = sys.exc_info()[0]
    email_message = ('''
    An error occurred while processing Radian6 to Salesforce export/import:

    {0}
    ''').format(str(e))
    msg = gmail.Message('ERROR: Radian6 to Salesforce',
                        to=', '.join(email_config['recipients']),
                        text=email_message)
    account.send(msg)
    raise


run_job()

