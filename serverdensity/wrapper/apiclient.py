# -*- coding: utf-8 -*-
import json

from requests import Session, Request
import requests
from serverdensity import __version__
from serverdensity.wrapper.exceptions import HttpError
from serverdensity.wrapper.exceptions import TimeoutError
from serverdensity.wrapper.exceptions import ClientError

from serverdensity.wrapper.device import Device
from serverdensity.wrapper.service import Service
from serverdensity.wrapper.alert import Alert
from serverdensity.wrapper.user import User
from serverdensity.wrapper.postback import Postback
from serverdensity.wrapper.dashboard import Dashboard
from serverdensity.wrapper.service_status import ServiceStatus


class ApiClient(object):

    VERSION = ''
    BASE_URL = 'https://api.serverdensity.io'

    def __init__(self, token, headers=None, timeout=(3, 5)):
        self.params = {'token': token}
        self.timeout = timeout
        self.headers = {'user-agent': 'SD Python Wrapper: {}'.format(__version__)}
        if headers:
            self.headers.update(headers)
        self._session = Session()
        self._devices = None
        self._services = None
        self._alerts = None
        self._service_status = None
        self._users = None
        self._postbacks = None
        self._dashboards = None


    @property
    def alerts(self):
        if not self._alerts:
            self._alerts = Alert(api=self)
        return self._alerts

    @property
    def devices(self):
        if not self._devices:
            self._devices = Device(api=self)
        return self._devices

    @property
    def dashboards(self):
        if not self._dashboards:
            self._dashboards = Dashboard(api=self)
        return self._dashboards

    @property
    def metrics(self):
        if not self._metrics:
            self._metrics = Metrics(api=self)
        return self._metrics

    @property
    def postbacks(self):
        if not self._postbacks:
            self._postbacks = Postback(api=self)
        return self._postbacks

    @property
    def services(self):
        if not self._services:
            self._services = Service(api=self)
        return self._services

    @property
    def service_status(self):
        if not self._service_status:
            self._service_status = ServiceStatus(api=self)
        return self._service_status

    @property
    def tags(self):
        if not self._tags:
            self._tags = Tags(api=self)
        return self._tags

    @property
    def users(self):
        if not self._users:
            self._users = User(api=self)
        return self._users




    def _stringify_dict_list(self, data):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                data[key] = json.dumps(value)
        return dict(data)


    def _make_request(self, method, url, data=None, params=None, **kwargs):
        if params:
            self.params.update(params)
        if kwargs.get('headers'):
            self.headers.update(kwargs['headers'])
        if data:
            data = self._stringify_dict_list(data)

        url = self.BASE_URL + self.VERSION + url
        req = Request(method, url, data=data, headers=self.headers, params=self.params)
        prepped = req.prepare()

        try:
            response = self._session.send(prepped, timeout=self.timeout)
            if response.status_code > 299:
                if 'message' in str(response.content):
                    response.reason += ': {}'.format(response.json()['message'])
                response.raise_for_status()
        except requests.HTTPError:
            msg = '{} {}'.format(response.status_code, response.reason)
            raise HttpError(msg)
        except requests.Timeout:
            raise TimeoutError('{} {} timed out after {} seconds'.format(
                method, url, self.timeout[0] + self.timeout[1]
            ))
        except requests.ConnectionError as e:
            raise ClientError('Could not reach: {} {} {}'.format(method, url, e))

        return response.json()

    def get(self, url, data=None, params=None, **kwargs):
        resp = self._make_request(method='GET', url=url, data=data, params=params, **kwargs)
        return resp

    def post(self, url, data=None, params=None, **kwargs):
        resp = self._make_request(method='POST', url=url, data=data, params=params, **kwargs)
        return resp

    def put(self, url, data=None, params=None, **kwargs):
        resp = self._make_request(method='PUT', url=url, data=data, params=params, **kwargs)
        return resp

    def delete(self, url, data=None, params=None, **kwargs):
        resp = self._make_request(method='DELETE', url=url, data=data, params=params, **kwargs)
        return resp

