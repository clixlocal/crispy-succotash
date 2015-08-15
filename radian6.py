import requests, pdb

# base_url = 'https://demo-api.radian6.com/socialcloud/v1'
base_url = 'https://api.radian6.com/socialcloud/v1'
auth_url = base_url + '/auth/authenticate'

headers = {
  'auth_user': 'matt@clixlocal.net',
  'auth_pass': '8@8yd@ddy'
}

response = requests.get(auth_url, headers=headers)
pdb.set_trace()
