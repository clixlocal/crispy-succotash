import requests, pdb
from xml.etree import ElementTree
from helpers import is_etree_list, etree_to_dict

base_url = 'https://demo-api.radian6.com/socialcloud/v1'
# base_url = 'https://api.radian6.com/socialcloud/v1'
auth_url = base_url + '/auth/authenticate'
topics_url = base_url + '/topics?type=1&basic=0&includeReactivation=true'
topics_params = {
  'type': 1,
  'basic': 0,
  'includeReactivation': True
}


auth_user = 'mstephen@clixsocial.com'
auth_pass = '6naGiants!'
auth_appkey = 'ppt7tnhrddh7n5uvm66fcsuk'
auth_token  = '0a0c02010308468f137ed42434255a3a85948713871a9dab9bb6517fad3d127b0d4502c8ae0d99650af42f15acf1ec2391744288016e'

# auth_headers = {
#   'auth_user':   auth_user,
#   'auth_appkey': auth_appkey,
#   'auth_pass':   auth_pass
# }
#
# response = requests.get(auth_url, headers=auth_headers)
# response_body = ElementTree.fromstring(response.content)
# auth_token = response_body.findall('token')[0].text

headers = {
  'auth_appkey': auth_appkey,
  'auth_token':  auth_token
}

response = requests.get(topics_url, headers=headers, params=topics_params)
print response.content
tree = ElementTree.fromstring(response.content)
parsed = etree_to_dict(tree)
topic_filter_ids = list(map(lambda t: t['topicFilterId'], parsed['topicFilters']))
# topic_filter_ids = list(map(lambda t: t.text, tree[0].findall('topicFilterId')))

pdb.set_trace()

# http://socialcloud.radian6.com/docs/read/socialcloud_reference/Data_Service#h2-get_post_data
# GET /data/topicdata/realtime/{recentXhours}/{topics}/{mediatypes}/{pageIndex}/{pageSize}

