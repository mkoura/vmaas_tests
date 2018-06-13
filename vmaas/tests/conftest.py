# -*- coding: utf-8 -*-

import logging

import pytest

from vmaas.rest import tools


logging.basicConfig()


def pytest_configure(config):
    config.addinivalue_line('markers', 'smoke: mark a test as a smoke test.')


@pytest.fixture()
def rest_api():
    return tools.rest_api()


@pytest.fixture(scope="session", autouse=True)
def cache_bash():
    """
    Each process of webapp has its own cache. Cache responses for bash
    package update request, with and without filters.
    Helps to catch https://github.com/RedHatInsights/vmaas/issues/306
    """

    rest_api = tools.rest_api()
    # cache response for plain bash updates
    request_body = tools.gen_updates_body(
        ['bash-0:4.2.46-20.el7_2.x86_64'])
    rest_api.get_updates(body=request_body).response_check()
    # cache reponse for bash updates with filter
    rest_api = tools.rest_api()
    request_body = tools.gen_updates_body(
        ['bash-0:4.2.46-20.el7_2.x86_64'], releasever='7Server')
    rest_api.get_updates(body=request_body).response_check()
