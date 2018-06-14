# -*- coding: utf-8 -*-

import logging

import pytest

from vmaas.misc import packages
from vmaas.rest import tools


logging.basicConfig()


def pytest_configure(config):
    config.addinivalue_line('markers', 'smoke: mark a test as a smoke test.')


@pytest.fixture()
def rest_api():
    return tools.rest_api()


@pytest.fixture(scope="session", autouse=True)
def cache_bash():
    """Cache responses for bash package update request, with and without filters.


    It *have to be run at the beginning of test suite* to cache response w/
    filters to one process and response w/o filters to the other one.
    Each process of webapp has its own cache.
    Application will cache response from tests otherwise and there could be
    same cached response if we don't run this first.

    Helps to catch https://github.com/RedHatInsights/vmaas/issues/306
    """

    rest_api = tools.rest_api()
    # cache response for plain bash updates
    request_body = tools.gen_updates_body([packages.CACHED_PKG])
    rest_api.get_updates(body=request_body).response_check()
    # cache reponse for bash updates with filter
    rest_api = tools.rest_api()
    request_body = tools.gen_updates_body(
        [packages.CACHED_PKG], releasever='7Server')
    rest_api.get_updates(body=request_body).response_check()
