# In this file, we will authenticate ourselves to the twitter api

import requests
import sys
import base64
import os

def base64encode(string):
    a = string.encode('utf-8')
    b = str(base64.b64encode(a))
    return b.split('\'')[1]

c_key = os.environ["TWITTER_KEY"]
c_secret = os.environ["TWITTER_SECRET"]
# URL_encode_them

#Base 64 encode secret+key to get a token
credentials = base64encode(c_key + ":" + c_secret)
# credentials = (c_key + ":" + c_secret).encode('utf-8')
# credentials = str(base64.b64encode(credentials))
# credentials = credentials.split('\'')[1]

url = "https://api.twitter.com/oauth2/token"
body = "grant_type=client_credentials"
headers = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8.',
    'Authorization': 'Basic {}'.format(credentials)}


r = requests.post(url, headers=headers, data=body)
if r.status_code == requests.codes.ok:
    token = r.json()
    bearer = token['access_token']
    auth_header = {'Authorization': 'Bearer {}'.format(bearer)}
    print('Bearer is {}'.format(bearer))
else:
    print('Could not get Twitter API token')
    sys.exit()

# We have a valid API bearer