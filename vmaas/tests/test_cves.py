# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import schemas, tools

EXP_2016_0634 = [
    {
        "cvss3_score": "4.9",
        "impact": "Moderate",
        "redhat_url": "https://access.redhat.com/security/cve/cve-2016-0634",
        "synopsis": "CVE-2016-0634"
    }
]

EXP_2014_7970 = [
    {
        "cvss3_score": "",
        "cwe_list": [
            "CWE-399"
        ],
        "impact": "Low",
        "redhat_url": "https://access.redhat.com/security/cve/cve-2014-7970",
        "secondary_url": "http://lists.opensuse.org/opensuse-security-announce/2015-04/msg00015.html",
        "synopsis": "CVE-2014-7970"
    }
]

EXP_2016_7970 = [
    {
        "cvss3_score": "7.500",
        "impact": "High",
        "secondary_url": "http://www.openwall.com/lists/oss-security/2016/10/05/2",
        "synopsis": "CVE-2016-7970"
    }
]

EXP_2016_7543 = [
    {
        "cvss3_score": "7",
        "impact": "Moderate",
        "redhat_url": "https://access.redhat.com/security/cve/cve-2016-7543",
        # "secondary_url": "http://rhn.redhat.com/errata/RHSA-2017-0725.html",
        "synopsis": "CVE-2016-7543"
    }
]

EXP_2016_7076 = [
    {
        "cvss3_score": "6.4",
        "impact": "Moderate",
        "redhat_url": "https://access.redhat.com/security/cve/cve-2016-7076",
        "synopsis": "CVE-2016-7076"
    }
]

EXP_2018_1000156 = [
    {
        "cvss3_score": "7.8",
        "impact": "Important",
        "redhat_url": "https://access.redhat.com/security/cve/cve-2018-1000156",
        "synopsis": "CVE-2018-1000156"
    }
]

# NOTE: all modified_dates for CVEs from RH source are modified date of latest CVE
CVES = [
    ('CVE-2016-0634', 'CVE-2016-0634', EXP_2016_0634),
    ('CVE-2014-7970', 'CVE-2014-7970', EXP_2014_7970),  # GH#211
    ('CVE-2016-7970', None, EXP_2016_7970),  # from NIST, not in RH
    ('CVE-2016-7543', 'CVE-2016-7543', EXP_2016_7543),
    ('CVE-2016-7076', 'CVE-2016-7076', EXP_2016_7076),  # GH#211, not in NIST, only in RH
    ('CVE-2018-1000156', 'CVE-2018-1000156', EXP_2018_1000156)
]


class TestCVEsQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple CVEs using POST."""
        request_body = tools.gen_cves_body([c[0] for c in CVES])
        cves = rest_api.get_cves(body=request_body).response_check()
        schemas.cves_schema.validate(cves.raw.body)
        assert len(cves) == len(CVES)
        for cve_name, _, _ in CVES:
            assert cve_name in cves

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_post_single(self, rest_api, cve_in):
        """Tests single CVE using POST."""
        cve_name, _, _ = cve_in
        request_body = tools.gen_cves_body([cve_name])
        cves = rest_api.get_cves(body=request_body).response_check()
        schemas.cves_schema.validate(cves.raw.body)
        assert len(cves) == 1
        cve, = cves
        assert cve.name == cve_name

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_get(self, rest_api, cve_in):
        """Tests single CVE using GET."""
        cve_name, _, _ = cve_in
        cves = rest_api.get_cve(cve_name).response_check()
        schemas.cves_schema.validate(cves.raw.body)
        assert len(cves) == 1
        cve, = cves
        assert cve.name == cve_name


class TestCVEsModifiedSince(object):
    def test_post_multi(self, rest_api):
        """Tests multiple CVEs using POST."""
        request_body = tools.gen_cves_body(
            [c[0] for c in CVES], modified_since='2018-01-01')
        cves = rest_api.get_cves(body=request_body).response_check()
        schemas.cves_schema.validate(cves.raw.body)
        assert len(cves) == len([c[1] for c in CVES if c[1]])
        for _, expected_name, _ in CVES:
            if expected_name:  # not None
                assert expected_name in cves

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_post_single(self, rest_api, cve_in):
        """Tests single CVE using POST."""
        cve_name, expected_name, _ = cve_in
        request_body = tools.gen_cves_body(
            [cve_name], modified_since='2018-01-01')
        cves = rest_api.get_cves(body=request_body).response_check()
        # don't validate schema on empty response
        if expected_name:
            schemas.cves_schema.validate(cves.raw.body)
            assert len(cves) == 1
            cve, = cves
            assert cve.name == expected_name
        else:
            assert len(cves) == 0
            assert not cves


class TestCVEsCorrect(object):
    def test_post_multi(self, rest_api):
        """Tests multiple CVEs using POST."""
        request_body = tools.gen_cves_body([c[0] for c in CVES])
        cves = rest_api.get_cves(body=request_body).response_check()
        assert len(cves) == len(CVES)
        for cve_name, _, expected in CVES:
            cve = cves[cve_name]
            tools.validate_cves(cve, expected)

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_post_single(self, rest_api, cve_in):
        """Tests single CVE using POST."""
        cve_name, _, expected = cve_in
        request_body = tools.gen_cves_body([cve_name])
        cves = rest_api.get_cves(body=request_body).response_check()
        assert len(cves) == 1
        cve, = cves
        tools.validate_cves(cve, expected)

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_get(self, rest_api, cve_in):
        """Tests single CVE using GET."""
        cve_name, _, expected = cve_in
        cves = rest_api.get_cve(cve_name).response_check()
        assert len(cves) == 1
        cve, = cves
        tools.validate_cves(cve, expected)
