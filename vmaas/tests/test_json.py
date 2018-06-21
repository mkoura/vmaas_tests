# -*- coding: utf-8 -*-

import pytest

from vmaas.utils.blockers import GH

UPDATES_JSON = {
    'package_list': [
        'bash-0:4.2.46-20.el7_2.x86_64'
    ],
    'repository_list': [
        'rhel-7-server-rpms'
    ],
    'releasever': '7Server',
    'basearch': 'x86_64'
}

CVES_JSON = {
    'cve_list': [
        'CVE-2017-57.*'
    ],
    'modified_since': '2018-04-05T01:23:45+02:00'
}

ERRATA_JSON = {
    'errata_list': [
        'RHSA-2018:05.*'
    ],
    'modified_since': '2018-01-01T01:23:45+02:00'
}

REPOS_JSON = {
    'repository_list': [
        'rhel-7-server-rpms',
        'rhel-7-workstation-rpms'
    ]
}

MALFORMED_JSON = "'key':'a quoted 'value' '"
EMPTY_JSON = {}

JSONS = [
    (UPDATES_JSON, 'updates', 'updates_json'),
    (CVES_JSON, 'cves', 'cves_json'),
    (ERRATA_JSON, 'errata', 'errata_json'),
    (REPOS_JSON, 'repos', 'repos_json'),
    (MALFORMED_JSON, None, 'malformed_json'),
    (EMPTY_JSON, None, 'empty_json'),
]


class TestJSON(object):
    @pytest.mark.parametrize('json', JSONS, ids=[j[2] for j in JSONS])
    def test_json_updates(self, rest_api, json):
        """Tests various json - /updates endpoint."""
        if json[1] == 'updates':
            updates = rest_api.get_updates(body=json[0]).response_check()
            assert 'available_updates' not in updates.raw.body
        else:
            updates = rest_api.get_updates(body=json[0]).response_check(400)
            assert 'available_updates' not in updates.raw.body

    @pytest.mark.skipif(GH(330).blocks or GH(329).blocks,
                        reason="blocked by GH#329 or GH#330")
    @pytest.mark.parametrize('json', JSONS, ids=[j[2] for j in JSONS])
    def test_json_cves(self, rest_api, json):
        """Tests various json - /cves endpoint."""
        if json[1] == 'cves':
            cves = rest_api.get_cves(body=json[0]).response_check()
            assert 'cve_list' in cves.raw.body
        else:
            cves = rest_api.get_cves(body=json[0]).response_check(400)
            assert 'cve_list' not in cves.raw.body

    @pytest.mark.skipif(GH(330).blocks or GH(329).blocks,
                        reason="blocked by GH#329 or GH#330")
    @pytest.mark.parametrize('json', JSONS, ids=[j[2] for j in JSONS])
    def test_json_errata(self, rest_api, json):
        """Tests various json - /errata endpoint."""
        if json[1] == 'errata':
            errata = rest_api.get_errata(body=json[0]).response_check()
            assert 'errata_list' in errata.raw.body
        else:
            errata = rest_api.get_errata(body=json[0]).response_check(400)
            assert 'errata_list' not in errata.raw.body

    @pytest.mark.skipif(GH(330).blocks or GH(329).blocks,
                        reason="blocked by GH#329 or GH#330")
    @pytest.mark.parametrize('json', JSONS, ids=[j[2] for j in JSONS])
    def test_json_repos(self, rest_api, json):
        """Tests various json - /repos endpoint."""
        if json[1] == 'repos':
            repos = rest_api.get_repos(body=json[0]).response_check()
            assert 'repository_list' in repos.raw.body
        else:
            repos = rest_api.get_repos(body=json[0]).response_check(400)
            assert 'repository_list' not in repos.raw.body
