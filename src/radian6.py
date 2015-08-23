import json, requests, pdb
from xml.etree import ElementTree
from src.helpers import is_etree_list, etree_to_dict

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
    return self.get(topics_url, params=topics_params)


