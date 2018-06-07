# -*- coding: utf-8 -*-

import logging

import pytest

from vmaas.rest.client import VMaaSClient
from vmaas.utils.conf import conf


logging.basicConfig()


def pytest_configure(config):
    config.addinivalue_line('markers', 'smoke: mark a test as a smoke test.')


@pytest.fixture()
def rest_api():
    hostname = conf.get('hostname', 'localhost')
    try:
        hostname, port = hostname.split(':')
    except ValueError:
        port = 8080 if hostname in ('localhost', '127.0.0.1') else 80
    return VMaaSClient(hostname, port=port)
