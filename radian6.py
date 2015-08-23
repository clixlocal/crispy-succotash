import requests, pdb
from xml.etree import ElementTree
from src.helpers import is_etree_list, etree_to_dict
from src.radian6 import Client

client = Client()
topics = client.get_topics()
topic_filter_ids = list(map(lambda t: t['topicFilterId'], topics['topicFilters']))
pdb.set_trace()

# http://socialcloud.radian6.com/docs/read/socialcloud_reference/Data_Service#h2-get_post_data
# GET /data/topicdata/realtime/{recentXhours}/{topics}/{mediatypes}/{pageIndex}/{pageSize}

