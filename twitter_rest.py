import requests
import base64
import os

auth_header = None
base_url = "https://api.twitter.com"

def base64encode(string):
    a = string.encode('utf-8')
    b = str(base64.b64encode(a))
    return b.split('\'')[1]

def authenticate():
    global auth_header
    c_key = os.environ["TWITTER_KEY"]
    c_secret = os.environ["TWITTER_SECRET"]
    credentials = base64encode(c_key + ":" + c_secret)

    url = base_url + "/oauth2/token"
    body = "grant_type=client_credentials"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8.',
        'Authorization': 'Basic {}'.format(credentials)}


    r = requests.post(url, headers=headers, data=body)
    if r.status_code == requests.codes.ok:
        token = r.json()
        bearer = token['access_token']
        auth_header = {'Authorization': 'Bearer {}'.format(bearer)}
        # print('Bearer is {}'.format(bearer))
        return True
    else:
        print('Could not get Twitter API token')
        return False

def get_retweets_by_id(id):
    url = base_url + "/1.1/statuses/retweeters/ids.json"
    params = {'id': str(id), 'count': '100', 'cursor': '-1'}
    r = requests.get(url, params=params, headers=auth_header)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        print("Could not get retweets")
        return None

def get_latest_tweet_by_id(id):
    url = base_url + "/1.1/statuses/user_timeline.json"
    params = {'id': str(id)}
    r = requests.get(url, params=params, headers=auth_header)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        print("Could not get latest tweet")
        return None