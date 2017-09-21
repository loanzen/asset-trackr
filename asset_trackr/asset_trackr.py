import json

from base64 import b64encode

import arrow

from attrdict import AttrDict

import requests


class AssetTrackrClient(object):
    def __init__(self, **kwargs):
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        if not self.username or not self.password:
            raise Exception('username or password not defined')
        self.headers = {
            'content-type': "application/x-www-form-urlencoded",
            'Authorization': 'Basic %s' % b64encode(self.username + ":" + self.password)
        }
        self.BASE_URL = "http://www.assettrackr.com"

    def add_new_device(self, serial_no, name):
        url = '{0}/assets/add_asset/auth_type/basic'.format(self.BASE_URL)

        payload = 'data=' + json.dumps({
            "sn": serial_no,
            "name": name,
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)

        return AttrDict(response.json())

    def list_all_devices(self):
        url = '{0}/assets/list_all_assets/auth_type/basic'.format(self.BASE_URL)

        response = requests.request("POST", url, headers=self.headers)

        return AttrDict(response.json())['success']

    def locate(self, serial_no):
        url = '{0}/assets/locate/sn/{1}/auth_type/basic'.format(self.BASE_URL, str(serial_no))
        response = requests.request("GET", url, headers=self.headers)

        return AttrDict(response.json())

    def trip(self, serial_no, date):
        url = '{0}/assets/trip/sn/{1}/date/{2}/auth_type/basic'.format(self.BASE_URL, str(serial_no), date)
        response = requests.request("GET", url, headers=self.headers)

        return AttrDict(response.json())

    def convert_history_format(self, history_obj):
        history_reformatted = {"result": []}
        history_obj = history_obj['result']
        for data_point in history_obj:
            history_reformatted['result'].append({
                'longitude': float(data_point['longitude']),
                'latitude': float(data_point['latitude']),
                'speed': float(data_point['speed']),
                'ignition_on': True if data_point['ignition_on'] == '1' else False,
                'odometer': int(float(data_point['odometer'])),
                'timestamp': arrow.get(data_point['datetime'], 'YYYY-MM-DD HH:mm:ss').datetime,
                'event_type': data_point['event_type'],
                'event_value': data_point['event_value']
            })
        return history_reformatted

    def history(self, serial_no, start_utime_local, end_utime_local):
        url = '{0}/assets/stretch/sn/{1}/start_utime_local/{2}/end_utime_local/{3}/auth_type/basic'.format(self.BASE_URL, str(serial_no), start_utime_local, end_utime_local)
        response = requests.request("GET", url, headers=self.headers)
        return AttrDict(self.convert_history_format(response.json()))['result']

    def create_geofence(self, serial_no, callback_url, fences):
        url = '{0}/assets/geofence/auth_type/basic'.format(self.BASE_URL)
        payload = 'data=' + json.dumps({
            "sn": serial_no,
            "callback_url": callback_url,
            "fences": fences,
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)

        return AttrDict(response.json())
