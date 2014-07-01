import requests
import json


class TinderClient(object):

    default_loc = {'lat': 37.78338563160064, 'lon':-122.4091201888036}

    def __init__(self, token=None, location=default_loc):
        self.token = token
        self.location = location
        self.last_moment_id = '523aa34354bfa7e87700148f9aca0c4c3cf547da95293270532e9058'
        self.last_activity_date = ''
        self.base_uri = 'https://api.gotinder.com'
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Tinder/4.0.3 (iPhone; iOS 7.1.1; Scale/2.00)',
            'os_version': '70000100001',
            'app_version': '88',
            'Accept': '*/*',
            'platform': 'ios',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate'
        }

        if self.token:
            self.headers['X-Auth-Token'] = self.token
            self.headers['Authorization'] = 'Token token="{}"'.format(self.token)

    def dislike(self, uid):
        self._get('pass/{}'.format(uid))

    def like(self, uid):
        return self._get('like/{}'.format(uid))['match']

    def get_likes(self):
        return self._post('feed/likes', {
            'last_moment_id': self.last_moment_id,
            # The last_activity_date always seems to empty when using this endpoint
            'last_activity_date': ''
        })['likes']

    def get_recs(self):
        return self._get('user/recs')

    def ping(self, location=default_loc):
        self.location = location
        self._post('user/ping', self.location)

    def _get(self, endpoint):
        target = '/'.join([self.base_uri, endpoint])
        r = requests.get(target, headers=self.headers)
        self._validate_http_res(r)
        return r.json()

    def _post(self, endpoint, data={}):
        target = '/'.join([self.base_uri, endpoint])
        r = requests.post(target, json.dumps(data), headers=self.headers)
        self._validate_http_res(r)
        return r.json()

    def _auth(self, fb_id, fb_token):
        target = self.base_uri + '/auth'
        data = json.dumps({
            'facebook_token': fb_token,
            'facebook_id': fb_id
        })
        r = requests.post(target, data, headers=self.headers)
        self._validate_http_res(r)
        res = r.json()
        self.token = res['token']
        self.headers['X-Auth-Token'] = self.token
        self.headers['Authorization'] = 'Token token="{}"'.format(self.token)

    def _validate_http_res(self, res):
        if not res.ok:
            raise TinderException(res.text, res.status_code)

class TinderException(Exception):

    def __init__(self, description, error_code=None):
        super(Exception, self).__init__(description)
        self.description = description
        self.error_code = error_code
