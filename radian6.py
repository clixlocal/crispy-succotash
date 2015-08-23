import requests, pdb, pprint
from src.radian6 import Client
from src.mappings import (
  media_types
)

pp = pprint.PrettyPrinter(indent=2)

client = Client()
topics = client.get_topics()
topic_filter_ids = list(map(lambda t: t['topicFilterId'], topics))
pp.pprint(topics)
pdb.set_trace()

# http://socialcloud.radian6.com/docs/read/socialcloud_reference/Data_Service#h2-get_post_data
# GET /data/topicdata/realtime/{recentXhours}/{topics}/{mediatypes}/{pageIndex}/{pageSize}


