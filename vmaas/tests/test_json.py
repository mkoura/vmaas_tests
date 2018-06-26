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
            assert isinstance(updates.raw.body, dict)
            assert 'available_updates' in updates[0]
        elif not json[1]:
            updates = rest_api.get_updates(body=json[0]).response_check(400)
            assert not isinstance(updates.raw.body, dict)
            if json[0]:
                assert "is not of type 'object'" in updates.raw.body
            else:
                assert 'Error: malformed input JSON' in updates.raw.body
        else:
            updates = rest_api.get_updates(body=json[0]).response_check(400)
            assert not isinstance(updates.raw.body, dict)
            assert "'package_list' is a required property" in updates.raw.body

    @pytest.mark.skipif(GH(330).blocks or GH(329).blocks,
                        reason="blocked by GH#329 or GH#330")
    @pytest.mark.parametrize('json', JSONS, ids=[j[2] for j in JSONS])
    def test_json_cves(self, rest_api, json):
        """Tests various json - /cves endpoint."""
        if json[1] == 'cves':
            cves = rest_api.get_cves(body=json[0]).response_check()
            assert isinstance(cves.raw.body, dict)
            assert 'cve_list' in cves.raw.body
        elif not json[1]:
            cves = rest_api.get_cves(body=json[0]).response_check(400)
            assert not isinstance(cves.raw.body, dict)
            if json[0]:
                assert "is not of type 'object'" in cves.raw.body
            else:
                assert 'Error: malformed input JSON' in cves.raw.body
        else:
            cves = rest_api.get_cves(body=json[0]).response_check(400)
            assert not isinstance(cves.raw.body, dict)
            assert "'cve_list' is a required property" in cves.raw.body

    @pytest.mark.skipif(GH(330).blocks or GH(329).blocks,
                        reason="blocked by GH#329 or GH#330")
    @pytest.mark.parametrize('json', JSONS, ids=[j[2] for j in JSONS])
    def test_json_errata(self, rest_api, json):
        """Tests various json - /errata endpoint."""
        if json[1] == 'errata':
            errata = rest_api.get_errata(body=json[0]).response_check()
            assert isinstance(errata.raw.body, dict)
            assert 'errata_list' in errata.raw.body
        elif not json[1]:
            errata = rest_api.get_errata(body=json[0]).response_check(400)
            assert not isinstance(errata.raw.body, dict)
            if json[0]:
                assert "is not of type 'object'" in errata.raw.body
            else:
                assert 'Error: malformed input JSON' in errata.raw.body
        else:
            errata = rest_api.get_errata(body=json[0]).response_check(400)
            assert not isinstance(errata.raw.body, dict)
            assert "'errata_list' is a required property" in errata.raw.body

    @pytest.mark.skipif(GH(330).blocks or GH(329).blocks,
                        reason="blocked by GH#329 or GH#330")
    @pytest.mark.parametrize('json', JSONS, ids=[j[2] for j in JSONS])
    def test_json_repos(self, rest_api, json):
        """Tests various json - /repos endpoint."""
        if json[1] in ['repos', 'updates']:
            repos = rest_api.get_repos(body=json[0]).response_check()
            assert isinstance(repos.raw.body, dict)
            assert 'repository_list' in repos.raw.body
        elif not json[1]:
            repos = rest_api.get_repos(body=json[0]).response_check(400)
            assert not isinstance(repos.raw.body, dict)
            if json[0]:
                assert "is not of type 'object'" in repos.raw.body
            else:
                assert 'Error: malformed input JSON' in repos.raw.body
        else:
            repos = rest_api.get_repos(body=json[0]).response_check(400)
            assert not isinstance(repos.raw.body, dict)
            assert "'repository_list' is a required property" in repos.raw.body
