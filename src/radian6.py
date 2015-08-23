import json, requests, pdb
from xml.etree import ElementTree
from src.helpers import (
  is_etree_list,
  etree_to_dict,
  unix_time_millis
)
from src.mappings import (
  report_media_type_ids
)

config_path = 'config/radian6.json'
config = json.load(open(config_path))

base_url = 'https://demo-api.radian6.com/socialcloud/v1'
# base_url = 'https://api.radian6.com/socialcloud/v1'

auth_url = base_url + '/auth/authenticate'
topics_url = base_url + '/topics'

class Client(object):
  def authenticate(self):
    response = requests.get(auth_url, headers={
      'auth_user':   config['auth_user'],
      'auth_appkey': config['auth_appkey'],
      'auth_pass':   config['auth_pass']
    })
    response_body = ElementTree.fromstring(response.content)
    config['auth_token'] = response_body.findall('token')[0].text
    json.dump(config, open(config_path))

  def get(self, url, headers={}, params={}):
    req_headers = {
      'auth_appkey': config['auth_appkey'],
      'auth_token':  config['auth_token']
    }
    req_headers.update(headers)
    response = requests.get(url, headers=req_headers, params=params)
    if response.status_code == 401:
      self.authenticate()
      response = requests.get(url, headers=req_headers, params=params)
    tree = ElementTree.fromstring(response.content)
    return etree_to_dict(tree)

  def get_topics(self):
    topics_params = {
      'type': 1,
      'basic': 0,
      'includeReactivation': True
    }
    return self.get(topics_url, params=topics_params)['topicFilters']

  def get_media_types(self):
    return self.get(base_url + '/lookup/mediaproviders')['MediaTypeList']

  def get_advanced_filter_types(self):
    return self.get(base_url + '/lookup/advancedfiltertypes')['AdvancedFilterTypeList']

  def get_regions(self):
    return self.get(base_url + '/lookup/regions')['Regions']

  def get_data_by_dates(self, start_date, end_date, topic_profile_id, page_size=10000):
    date_range_start = str(int(unix_time_millis(start_date)))
    date_range_end   = str(int(unix_time_millis(end_date)))
    format_params = {
      'date_range_start': date_range_start,
      'date_range_end': date_range_end,
      'topics': topic_profile_id,
      'media_types': ','.join(report_media_type_ids),
      'page_size': page_size
    }
    data_url = '/data/topicdata/realtime/{date_range_start}/{date_range_end}/{topics}/{media_types}/{page_index}/{page_size}'
    params = {
      # 'keywordGroups': '1',
      # 'advancedFilters': '' # TODO: figure out how to provide filters for KeywordGroups and Regions
    }
    responses = []
    start_params = format_params.copy()
    start_params.update({'page_index': 1})
    start_url = base_url + data_url.format(**start_params)
    start_response = self.get(start_url, params=params)['radian6_RiverOfNews_export']
    responses.append(start_response)
    return responses

class Radian6Data(object):
  def __init__(self, client):
    self.client = client
    self.topics = []

  def topic_profile(self, topic_profile_name='Hospitals'):
    if not self.topics:
      self.topics = self.client.get_topics()
    filtered_topics = list(filter(lambda t: t['topicFilter']['name'] == topic_profile_name, self.topics))
    return filtered_topics[0]['topicFilter']

  def topic_profile_id(self, topic_profile_name='Hospitals'):
    topic_profile = self.topic_profile(topic_profile_name)
    return topic_profile['topicFilterId']

  def filter_groups(self, topic_profile_name='Hospitals'):
    topic_profile = self.topic_profile(topic_profile_name)
    groups = topic_profile['filterGroups']['filterGroups']
    return {fg['name']: fg['filterGroupId'] for fg in groups}

