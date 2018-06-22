# -*- coding: utf-8 -*-

import iso8601

from time import sleep
from vmaas.rest import tools


class TestDBChange(object):
    def test_dbchange(self, rest_api):
        """Tests that dates in db are changing after /sync"""
        response = rest_api.get_dbchange().response_check()
        cve = iso8601.parse_date(response.raw.body['cve_changes'])
        last = iso8601.parse_date(response.raw.body['last_change'])
        errata = iso8601.parse_date(response.raw.body['errata_changes'])
        exported = iso8601.parse_date(response.raw.body['exported'])
        repo = iso8601.parse_date(response.raw.body['repository_changes'])

        # perform sync /api/v1/sync
        tools.sync_all()
        # wait for sync
        sleep(30)

        # get datetimes after sync
        response = rest_api.get_dbchange().response_check()
        cve2 = iso8601.parse_date(response.raw.body['cve_changes'])
        last2 = iso8601.parse_date(response.raw.body['last_change'])
        errata2 = iso8601.parse_date(response.raw.body['errata_changes'])
        exported2 = iso8601.parse_date(response.raw.body['exported'])
        repo2 = iso8601.parse_date(response.raw.body['repository_changes'])

        assert cve2 >= cve
        assert last2 >= last
        assert errata2 == errata    # from repolist.json, should remain same
        assert exported2 > exported
        assert repo2 == repo    # from repolist.json, should remain same
