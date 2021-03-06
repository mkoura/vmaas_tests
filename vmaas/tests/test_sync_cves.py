# -*- coding: utf-8 -*-

import pytest

from wait_for import wait_for

from vmaas.rest import exceptions


@pytest.mark.skip(reason='not testing sync')
def test_sync_cves(rest_api):
    def _refresh():
        try:
            response = rest_api.cvescan()
        except exceptions.ClientError as err:
            if 'Another sync task already in progress' in err.response.body['msg']:
                return False
            raise
        return response

    response, __ = wait_for(_refresh, num_sec=10)
    response.response_check()
    response, = response
    assert 'CVE sync task started' in response.msg
