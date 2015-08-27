import json, requests, pdb
from requests import Request, Session
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

  def get(self, url, headers={}, params={}, xml_to_dict=True, extra_query_params=None):
    req_headers = {
      'auth_appkey': config['auth_appkey'],
      'auth_token':  config['auth_token']
    }
    req_headers.update(headers)
    req = Request('GET', url, headers=req_headers, params=params)
    sess = Session()
    #response = requests.get(url, headers=req_headers, params=params)
    prepped = req.prepare()
    if extra_query_params:
      prepped.url = prepped.url + "&" + extra_query_params
    response = sess.send(prepped)
    pdb.set_trace()
    if response.status_code == 401:
      self.authenticate()
      response = requests.get(url, headers=req_headers, params=params)
    if xml_to_dict:
      tree = ElementTree.fromstring(response.content)
      return etree_to_dict(tree)
    else:
      return response.content

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

  def get_count_types(self):
    return self.get(base_url + '/lookup/counttypes')['CountTypeList']

  def get_data_by_dates(self, start_date, end_date, topic_profile_id, page_size=10000, keyword_group_ids=None):
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
      'keywordGroups': '1',
      # 'advancedFilters': '' # TODO: figure out how to provide filters for KeywordGroups and Regions
    }
    advanced_filters = None
    if keyword_group_ids:
      #advanced_filters = 'advancedFilters=' + '|'.join(['9:{0}'.format(kg_id) for kg_id in keyword_group_ids])
      advanced_filters = '|'.join(['9:{0}'.format(kg_id) for kg_id in keyword_group_ids])
      params['advancedFilters'] = advanced_filters
    responses = []
    start_params = format_params.copy()
    start_params.update({'page_index': 1})
    start_url = base_url + data_url.format(**start_params)
    start_response = self.get(start_url, params=params)['radian6_RiverOfNews_KeywordGrouped_export']
    responses.append(start_response)
    # TODO: Add pagination logic, if start_response['total_article_count'] > page_size
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
    return {fg['filterGroup']['filterGroupId']: fg['filterGroup']['name'] for fg in groups}

