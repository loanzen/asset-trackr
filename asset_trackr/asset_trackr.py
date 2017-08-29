import requests
from attrdict import AttrDict
from base64 import b64encode
import json


class AssetTrackrClient(object):
    def __init__(self, **kwargs):
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)

    BASE_URL = "http://www.assettrackr.com"

    def add_new_device(self, serial_no, name):
        url = '{0}/assets/add_asset/auth_type/basic'.format(self.BASE_URL)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'Authorization': 'Basic %s' % b64encode(self.username + ":" + self.password)
        }
        payload = 'data=' + json.dumps({
            "sn": serial_no,
            "name": name,
        })
        response = requests.request("POST", url, headers=headers, data=payload)

        return AttrDict(response.json())

    def locate(self, serial_no):
        url = '{0}/assets/locate/sn/{1}/auth_type/basic'.format(self.BASE_URL, str(serial_no))
        headers = {'Authorization': 'Basic %s' % b64encode(self.username + ":" + self.password)}
        response = requests.request("GET", url, headers=headers)

        return AttrDict(response.json())

    def trip(self, serial_no, date):
        url = '{0}/assets/trip/sn/{1}/date/{2}/auth_type/basic'.format(self.BASE_URL, str(serial_no), date)
        headers = {'Authorization': 'Basic %s' % b64encode(self.username + ":" + self.password)}
        response = requests.request("GET", url, headers=headers)

        return AttrDict(response.json())

    def history(self, serial_no, start_utime_local, end_utime_local):
        url = '{0}/assets/stretch/sn/{1}/start_utime_local/{2}/end_utime_local/{3}/auth_type/basic'.format(self.BASE_URL, str(serial_no), start_utime_local, end_utime_local)
        headers = {'Authorization': 'Basic %s' % b64encode(self.username + ":" + self.password)}
        response = requests.request("GET", url, headers=headers)

        return AttrDict(response.json())

    def create_geofence(self, serial_no, callback_url, fences):
        url = '{0}/assets/geofence/auth_type/basic'.format(self.BASE_URL)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'Authorization': 'Basic %s' % b64encode(self.username + ":" + self.password)
        }
        payload = 'data=' + json.dumps({
            "sn": serial_no,
            "callback_url": callback_url,
            "fences": fences,
        })
        response = requests.request("POST", url, headers=headers, data=payload)

        return AttrDict(response.json())
