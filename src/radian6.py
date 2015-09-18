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

#base_url = 'https://demo-api.radian6.com/socialcloud/v1'
base_url = 'https://api.radian6.com/socialcloud/v1'

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
    with open(config_path, 'w+') as config_file:
      json.dump(config, config_file, indent=2)

  def req_headers(self):
    return {
      'auth_appkey': config['auth_appkey'],
      'auth_token':  config['auth_token']
    }

  def get(self, url, headers={}, params={}, xml_to_dict=True, extra_query_params=None):
    req_headers = self.req_headers()
    req_headers.update(headers)
    req = Request('GET', url, headers=req_headers, params=params)
    sess = Session()
    #response = requests.get(url, headers=req_headers, params=params)
    prepped = req.prepare()
    if extra_query_params:
      if "?" in prepped.url:
        prepped.url = prepped.url + "&" + extra_query_params
      else:
        prepped.url = prepped.url + "?" + extra_query_params
    response = sess.send(prepped)
    if response.status_code == 401:
      self.authenticate()
      req_headers.update(self.req_headers())
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

  def get_post_details(self, post_url):
    params = {
      'url': post_url
    }
    return self.get(base_url + '/post', params=params).get('PostDetails')

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
    return self._get_data(data_url, format_params, keyword_group_ids)

  def get_data_by_hours(self, hours, topic_profile_id, page_size=10000, keyword_group_ids=None):
    format_params = {
      'hours': hours,
      'topics': topic_profile_id,
      'media_types': ','.join(report_media_type_ids),
      'page_size': page_size
    }
    data_url = '/data/topicdata/realtime/{hours}/{topics}/{media_types}/{page_index}/{page_size}'
    return self._get_data(data_url, format_params, keyword_group_ids)

  def _get_data(self, url, format_params, keyword_group_ids):
    params = {}
    advanced_filters = None
    if keyword_group_ids:
      advanced_filters = 'advancedFilters=' + '|'.join(['9:"{0}"'.format(kg_id) for kg_id in keyword_group_ids])
      top_level_element = 'radian6_RiverOfNews_export'
    else:
      # TODO: keywordGroups param must NOT be included for the advancedFilters param to work
      top_level_element = 'radian6_RiverOfNews_KeywordGrouped_export'
      params['keywordGroups'] = '1'

    responses = []
    start_params = format_params.copy()
    start_params.update({'page_index': 1})
    start_url = base_url + url.format(**start_params)
    start_response = self.get(start_url, params=params, extra_query_params=advanced_filters)[top_level_element]
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
    return {fg['filterGroup']['name']: fg['filterGroup']['filterGroupId'] for fg in groups}

