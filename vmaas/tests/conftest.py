# -*- coding: utf-8 -*-

import logging

import pytest

from vmaas.rest import tools
from vmaas.rest.client import VMaaSClient
from vmaas.utils.conf import conf


logging.basicConfig()


def pytest_configure(config):
    config.addinivalue_line('markers', 'smoke: mark a test as a smoke test.')


@pytest.fixture(name='make_conn')
def _make_conn():
    def make_conn():
        hostname = conf.get('hostname', 'localhost')
        try:
            hostname, port = hostname.split(':')
        except ValueError:
            port = 8080 if hostname in ('localhost', '127.0.0.1') else 80
        return VMaaSClient(hostname, port=port)

    yield make_conn


@pytest.fixture()
def rest_api(make_conn):
    return make_conn()


@pytest.fixture(scope="session", autouse=True)
def cache_bash():
    """
    Each process of webapp has its own cache. Cache responses for bash
    package update request, with and without filters.
    Helps to catch https://github.com/RedHatInsights/vmaas/issues/306
    """

    hostname = conf.get('hostname', 'localhost')
    try:
        hostname, port = hostname.split(':')
    except ValueError:
        port = 8080 if hostname in ('localhost', '127.0.0.1') else 80
    rest_api = VMaaSClient(hostname, port=port)

    # cache response for plain bash updates
    request_body = tools.gen_updates_body(
        ['bash-0:4.2.46-20.el7_2.x86_64'])
    rest_api.get_updates(body=request_body).response_check()
    # cache reponse for bash updates with filter
    rest_api = VMaaSClient(hostname, port=port)
    request_body = tools.gen_updates_body(
        ['bash-0:4.2.46-20.el7_2.x86_64'], releasever='7Server')
    rest_api.get_updates(body=request_body).response_check()
