import requests, pdb, pprint, datetime
from src.radian6 import Client, Radian6Data
from src.mappings import (
  media_types
)

pp = pprint.PrettyPrinter(indent=2)

client = Client()
rd6_data = Radian6Data(client)
# topics = client.get_topics()
# topic_filter_ids = list(map(lambda t: t['topicFilterId'], topics))
start_date = datetime.datetime.strptime('2015-08-17', '%Y-%m-%d')
end_date = datetime.datetime.strptime('2015-08-21', '%Y-%m-%d')
topic_profile_id = rd6_data.topic_profile_id()
topic_analysis_data = client.get_data_by_dates(start_date, end_date, topic_profile_id)
pp.pprint(topic_analysis_data)
pdb.set_trace()

# filter_groups = rd6_data.filter_groups()
# pp.pprint(filter_groups)
pdb.set_trace()

# http://socialcloud.radian6.com/docs/read/socialcloud_reference/Data_Service#h2-get_post_data
# GET /data/topicdata/realtime/{recentXhours}/{topics}/{mediatypes}/{pageIndex}/{pageSize}
# GET /data/topicdata/realtime/{daterangeStart}/{daterangeEnd}/{topics}/{mediatypes}/{pageIndex}/{pageSize}


