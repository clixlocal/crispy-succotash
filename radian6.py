import requests, pdb, pprint, datetime, csv
from src.radian6 import Client, Radian6Data
from src.mappings import (
  media_types
)

pp = pprint.PrettyPrinter(indent=2)

client = Client()
rd6_data = Radian6Data(client)

start_date = datetime.datetime.strptime('2015-08-17', '%Y-%m-%d')
end_date = datetime.datetime.strptime('2015-08-21', '%Y-%m-%d')
topic_profile_id = rd6_data.topic_profile_id()
filter_groups = rd6_data.filter_groups()
# ['FG_94261', 'FG_94260', 'FG_94253', 'FG_94254', 'FG_94255', 'FG_94256', 'FG_94257', 'FG_94258', 'FG_94259']
pdb.set_trace()

topic_analysis_data = client.get_data_by_dates(start_date, end_date, topic_profile_id, keyword_group_ids=['94261'])[0]

# [3:] trims off the leading 'FG_'
keyword_group_data = {g['KeywordGroupData']['id'][3:]: g['KeywordGroupData']['content'] for g in topic_analysis_data}

total_articles = {kgid: len(kg[0]['radian6_RiverOfNews_export'].get('article')) for (kgid, kg) in keyword_group_data.items() if kg[0]['radian6_RiverOfNews_export'].get('article') }
pp.pprint(total_articles)

pdb.set_trace()

article = topic_analysis_data['article'][0]
pp.pprint(article)

api_file = open('data/api_file.csv', 'wb')
fieldnames = ['ARTICLE_ID','HEADLINE','AUTHOR','CONTENT','ARTICLE_URL','MEDIA_PROVIDER','PUBLISH_DATE','VIEW_COUNT','COMMENT_COUNT','UNIQUE_COMMENTERS','ENGAGEMENT','LIKES_AND_VOTES','INBOUND_LINKS','FORUM_THREAD_SIZE','FOLLOWING','FOLLOWERS','UPDATES','BLOG_POST_SENTIMENT','BLOG_POST_ENGAGEMENT','BLOG_POST_CLASSIFICATION','BLOG_POST_ASSIGNMENT','BLOG_POST_PRIORITY','BLOG_POST_COMMENT','BLOG_POST_NOTE','BLOG_POST_TAG','BLOG_SOURCE_TAG','FIRST_ENGAGEMENT_ACTIVITY','LAST_ENGAGEMENT_ACTIVITY']
api_writer = csv.DictWriter(api_file, fieldnames=fieldnames)
api_writer.writeheader()
for tp_data in topic_analysis_data:
  for article in tp_data['article']:
    description = article['description']['description']
    pdd = article['PostDynamicsIteration']['PostDynamicsIteration']['PostDynamicsDefinition']
    pdd = {f['label']: f['value'] for f in pdd}

    row = {
      'ARTICLE_ID':        article['ID'],
      'HEADLINE':          description['headline'],
      'AUTHOR':            description['author'],
      'CONTENT':           description['content'],
      'ARTICLE_URL':       article['article_url'],
      'MEDIA_PROVIDER':    article['media_provider'],
      'PUBLISH_DATE':      article['publish_date'],
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
    row = {key: str.encode('utf8') if isinstance(val, unicode) else val for key, val in row.items()}
    api_writer.writerow(row)



# http://socialcloud.radian6.com/docs/read/socialcloud_reference/Data_Service#h2-get_post_data
# GET /data/topicdata/realtime/{recentXhours}/{topics}/{mediatypes}/{pageIndex}/{pageSize}
# GET /data/topicdata/realtime/{daterangeStart}/{daterangeEnd}/{topics}/{mediatypes}/{pageIndex}/{pageSize}


