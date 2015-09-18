import requests, pdb, pprint, datetime, csv, json, boto3, argparse, sys, io, twitter, re, time
sys.path.append('.')
from src.radian6 import Client, Radian6Data
from src.mappings import (
  media_types,
  barnabas_daily_keywords
)
from cStringIO import StringIO

parser = argparse.ArgumentParser(description='Pull down keyword group data from radian6 and upload to s3')
parser.add_argument('--hours', type=str, help='The number of hours to pull for the last posts.', default='12')
parser.add_argument('s3_folder', type=str, help='The s3 folder to place the files in.')

args = parser.parse_args()

aws_config = json.load(open('config/aws.json'))
boto3.setup_default_session(**aws_config)
s3 = boto3.resource('s3')
crispy_bucket = s3.Bucket('crispy-succotash')

twitter_config = json.load(open('config/twitter.json'))
twitter_api = twitter.Api(**twitter_config)

pp = pprint.PrettyPrinter(indent=2)

client = Client()
rd6_data = Radian6Data(client)

start_date = datetime.datetime.strptime('2015-09-16 16:00:00', '%Y-%m-%d %H:%M:%S')
end_date = datetime.datetime.strptime('2015-09-17 16:00:00', '%Y-%m-%d %H:%M:%S')
#end_date = datetime.datetime.now()
topic_profile_id = rd6_data.topic_profile_id()
filter_groups = rd6_data.filter_groups()
# ['FG_94261', 'FG_94260', 'FG_94253', 'FG_94254', 'FG_94255', 'FG_94256', 'FG_94257', 'FG_94258', 'FG_94259']

for (keyword, filename) in barnabas_daily_keywords.items():
  keyword_group_id = filter_groups.get(keyword)
  if not keyword_group_id:
    print('Missing filter group for: ' + keyword)
    continue
  if not filename:
    print('Missing filename for: ' + keyword)
    continue

  keyword_group_id = 'FG_' + keyword_group_id

  # topic_analysis_data = client.get_data_by_dates(start_date, end_date, topic_profile_id, keyword_group_ids=[keyword_group_id])[0]
  topic_analysis_data = client.get_data_by_hours(args.hours, topic_profile_id, keyword_group_ids=[keyword_group_id])[0]

  if int(topic_analysis_data['article_count']) == 0:
    print('no articles for ' + keyword)
    total_articles = 0
  else:
    total_articles = len(topic_analysis_data['article'])
    print("total articles for {0}: ".format(keyword) + str(total_articles))


  api_file = StringIO()
  fieldnames = ['ARTICLE_ID','HEADLINE','AUTHOR','CONTENT','ARTICLE_URL','MEDIA_PROVIDER','PUBLISH_DATE','VIEW_COUNT','COMMENT_COUNT','UNIQUE_COMMENTERS','ENGAGEMENT','LIKES_AND_VOTES','INBOUND_LINKS','FORUM_THREAD_SIZE','FOLLOWING','FOLLOWERS','UPDATES','BLOG_POST_SENTIMENT','BLOG_POST_ENGAGEMENT','BLOG_POST_CLASSIFICATION','BLOG_POST_ASSIGNMENT','BLOG_POST_PRIORITY','BLOG_POST_COMMENT','BLOG_POST_NOTE','BLOG_POST_TAG','BLOG_SOURCE_TAG','FIRST_ENGAGEMENT_ACTIVITY','LAST_ENGAGEMENT_ACTIVITY']
  api_writer = csv.DictWriter(api_file, fieldnames=fieldnames)
  api_writer.writeheader()

  def process_article(article):
    description = article['description']['description']

    pdd = article['PostDynamicsIteration']['PostDynamicsIteration']['PostDynamicsDefinition']
    if type(pdd) == list:
      pdd = {f['label']: f['value'] for f in pdd}
    elif type(pdd) == dict:
      pdd = pdd['PostDynamicsDefinition']
      pdd = {pdd['label']: pdd['value']}

    content = description['content']['content'] if type(description['content']) == dict else description['content']
    if not content and article['article_url'] and article['media_provider'] == 'TWITTER':
      twitter_url_match = re.search('statuses\/(.+)$', article['article_url'])
      if twitter_url_match:
        status_id = twitter_url_match.group(1)
        print('pulling data for twitter_url: ' + article['article_url'] + ' status_id: ' + status_id)
        try:
          tweet_status = twitter_api.GetStatus(status_id)
          content = tweet_status.text.encode('utf8')
          author  = tweet_status.user.screen_name.encode('utf8')
          headline = "TWEET FROM: {0}".format(author)
          # Rate Limiting: https://dev.twitter.com/rest/public/rate-limits
          time.sleep(5) # For rate limiting, 180 requests per 15 min. == 1 request per 5 secs.
        except twitter.error.TwitterError as e:
          print(e)
          time.sleep(5) # For rate limiting, 180 requests per 15 min. == 1 request per 5 secs.
          return
      else:
        raise "twitter status url format change: " + article['article_url']
    else:
      author = description['author']['content']
      headline = description['headline']

    row = {
      'ARTICLE_ID':        article.get('ID'),
      'HEADLINE':          headline,
      'AUTHOR':            author,
      'CONTENT':           content,
      'ARTICLE_URL':       article['article_url'],
      'MEDIA_PROVIDER':    article['media_provider'],
      'PUBLISH_DATE':      article['publish_date']['content'],
      'VIEW_COUNT':        pdd.get('View Count'),
      'COMMENT_COUNT':     pdd.get('Comment Count'),
      'UNIQUE_COMMENTERS': pdd.get('Unique Source Count'),
      'ENGAGEMENT':        None,
      'LIKES_AND_VOTES':   pdd.get('Likes and Votes'),
      'INBOUND_LINKS':     pdd.get('Total Inbound Links'),
      'FORUM_THREAD_SIZE': None,
      'FOLLOWING':         pdd.get('Following'),
      'FOLLOWERS':         pdd.get('Followers'),
      'UPDATES':           pdd.get('Updates'),
      'BLOG_POST_SENTIMENT':       None,
      'BLOG_POST_ENGAGEMENT':      None,
      'BLOG_POST_CLASSIFICATION':  None,
      'BLOG_POST_ASSIGNMENT':      None,
      'BLOG_POST_PRIORITY':        None,
      'BLOG_POST_COMMENT':         None,
      'BLOG_POST_NOTE':            None,
      'BLOG_POST_TAG':             None,
      'BLOG_SOURCE_TAG':           None,
      'FIRST_ENGAGEMENT_ACTIVITY': None,
      'LAST_ENGAGEMENT_ACTIVITY':  None
    }
    row = {key: val.encode('utf8') if isinstance(val, unicode) else val for key, val in row.items()}
    api_writer.writerow(row)


  if total_articles > 1:
    [process_article(a) for a in topic_analysis_data['article']]
  elif total_articles == 1:
    process_article(topic_analysis_data['article']['article'])

  s3_object_name = args.s3_folder + filename + '.csv'
  crispy_bucket.put_object(Key=s3_object_name, Body=api_file.getvalue())
  api_file.close()
  print("Done processing and uploaded for {0}".format(keyword))

# http://socialcloud.radian6.com/docs/read/socialcloud_reference/Data_Service#h2-get_post_data
# GET /data/topicdata/realtime/{recentXhours}/{topics}/{mediatypes}/{pageIndex}/{pageSize}
# GET /data/topicdata/realtime/{daterangeStart}/{daterangeEnd}/{topics}/{mediatypes}/{pageIndex}/{pageSize}


