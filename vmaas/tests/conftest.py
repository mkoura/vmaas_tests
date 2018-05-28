# -*- coding: utf-8 -*-

import logging

import pytest

from vmaas.rest.client import VMaaSClient
from vmaas.utils.conf import conf


logging.basicConfig()


@pytest.fixture()
def rest_api():
    hostname = conf.get('hostname', 'localhost')
    try:
        hostname, port = hostname.split(':')
    except ValueError:
        port = 8080
    return VMaaSClient(hostname, port=port)
