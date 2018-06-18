# -*- coding: utf-8 -*-
# pylint: disable=no-member
"""
VMaaS REST API client for tests development.
"""

import logging

from simple_rest_client.api import API as SimpleAPI
from simple_rest_client.resource import Resource as SimpleResource

import iso8601


class QueryApiActions(SimpleResource):
    """Actions available on query API."""
    actions = {
        'get_cve': {'method': 'GET', 'url': 'cves/{}'},
        'get_cves': {'method': 'POST', 'url': 'cves'},
        'get_erratum': {'method': 'GET', 'url': 'errata/{}'},
        'get_errata': {'method': 'POST', 'url': 'errata'},
        'get_repo': {'method': 'GET', 'url': 'repos/{}'},
        'get_repos': {'method': 'POST', 'url': 'repos'},
        'get_update': {'method': 'GET', 'url': 'updates/{}'},
        'get_updates': {'method': 'POST', 'url': 'updates'},
    }


class SyncApiActions(SimpleResource):
    """Actions available on sync API."""
    actions = {
        'cvescan': {'method': 'GET', 'url': 'sync/cve'},
        'reposcan': {'method': 'POST', 'url': 'sync/repo'},
        'reporefresh': {'method': 'GET', 'url': 'sync/repo'},
    }


class VMaaSClient(object):
    """VMaaS REST API client.

    Args:
        address: IP address or hostname of query service
        port: Port of query service
        address2: IP address or hostname of sync service
        port2: Port of sync service
        logger: Instance of logger
    """
    # pylint: disable=too-many-arguments
    def __init__(self, address, port=8080, address2=None, port2=8081, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.query_api = SimpleAPI(
            api_root_url='http://{}:{}/api/v1/'.format(address, port),  # base api url
            params={},  # default params
            headers={},  # default headers
            timeout=2,  # default timeout in seconds
            append_slash=False,  # append slash to final url
            json_encode_body=True,  # encode body as json
        )
        self.sync_api = SimpleAPI(
            api_root_url='http://{}:{}/api/v1/'.format(address2 or address, port2),
            params={},
            headers={},
            timeout=2,
            append_slash=False,
            json_encode_body=True,
        )

        self.query_api.add_resource(resource_name='actions', resource_class=QueryApiActions)
        self.sync_api.add_resource(resource_name='actions', resource_class=SyncApiActions)

        for action in QueryApiActions.actions:
            setattr(self, action, self._wrap_action(self.query_api.actions, action))
        for action in SyncApiActions.actions:
            setattr(self, action, self._wrap_action(self.sync_api.actions, action))

        setattr(self, 'all_actions', self.query_api.actions.actions)
        setattr(self, 'all_sync_actions', self.sync_api.actions.actions)

    @staticmethod
    def _wrap_action(api_obj, action_name):
        action = getattr(api_obj, action_name)

        def wrapper(*args, **kwargs):
            response = action(*args, **kwargs)
            return ResponseContainer(response)

        return wrapper


class ResponseContainer(object):
    """Holds response data and Resources created out of response data.

    Args:
        response: Complete response as returned by simple_rest_client
    """
    def __init__(self, response):
        self.raw = response
        self._resources_dict = {}
        self._resources_list = []
        self.load()

    def load(self):
        """Loads response body data."""
        body = self.raw.body
        if not body:
            return self

        self._resources_dict = {}
        self._resources_list = []

        data_dict = {}
        if 'update_list' in body:
            data_dict = body['update_list']
        elif 'errata_list' in body:
            data_dict = body['errata_list']
        elif 'repository_list' in body:
            data_dict = body['repository_list']
        elif 'cve_list' in body:
            data_dict = body['cve_list']
        else:
            data_dict = {'Bare': body}

        for item in data_dict:
            res = Resource(item, body=data_dict[item])
            self._add_resource(item, res)

        return self

    def _add_resource(self, name, val):
        self._resources_list.append(val)
        self._resources_dict[name] = val

    def response_check(self, status_code=None):
        """Asserts that the response HTTP status code and content is as expected."""
        if status_code:
            assert self.raw.status_code == status_code
        else:
            assert self.raw.client_response

        assert isinstance(
            self.raw.body, dict), 'Response is not JSON:\n'r'{}'.format(self.raw.body)

        if 'success' in self.raw.body:
            assert self.raw.body['success']

        return self

    def get(self, key, default_value=None):
        return self._resources_dict.get(key, default_value)

    def __iter__(self):
        return iter(self._resources_list)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._resources_dict[item]
        return self._resources_list[item]

    def __len__(self):
        return len(self._resources_list)

    def __contains__(self, item):
        return item in self._resources_dict

    def __repr__(self):
        return repr(self._resources_list)


class Resource(object):
    """Holds processed part of response data.

    Args:
        name: Name of the resource (e.g. bash-0:4.2.46-20.el7_2.x86_64)
        body: Resource data
    """
    TIME_FIELDS = {
        'public_date', 'modified_date', 'updated', 'issued'
    }

    def __init__(self, name, body=None):
        self.name = name
        # set the same with underscore to make sure
        # it's not overriden by ``self.load()``
        self._name = name
        self.raw = body
        self._body = body
        self.load()

    def load(self):
        """Loads resource body data."""
        if not isinstance(self.raw, dict):
            return self

        self._body = self.raw.copy()

        for key, value in self.raw.items():
            self._set_key(key, value)

        return self

    def _set_key(self, key, value):
        if value and key in self.TIME_FIELDS:
            value = iso8601.parse_date(value)
            self._body[key] = value
        setattr(self, key, value)

    def __iter__(self):
        return iter(self._body)

    def __getattr__(self, attr):
        return getattr(self._body, attr)

    def __getitem__(self, item):
        return self._body[item]

    def __len__(self):
        return len(self._body)

    def __contains__(self, item):
        return item in self._body

    def __repr__(self):
        return '<Resource {}>'.format(self._name)
