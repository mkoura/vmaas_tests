# -*- coding: utf-8 -*-

# TODO: - pagination
#       e.g. I expect 100 CVEs are returned, set page_size=40,
#       first page contains 40 CVEs, 2nd page - 40 CVEs, 3rd page - 20 CVEs
#       same test needed for test_errata

import pytest

from vmaas.rest import schemas, tools
from vmaas.utils.blockers import GH


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
        "secondary_url":
            "http://lists.opensuse.org/opensuse-security-announce/2015-04/msg00015.html",
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

# CVEs for negative testing
CVES_NEG = [
    ('CVE-9999-9999', None, None),
    ('', None, None)
]
# NOTE: all modified_dates for CVEs from RH source are modified date of latest CVE
# if you add negative test for CVE which doesn't exist in DB,
# please add same line to CVES_NEG list
CVES = [
    ('CVE-2016-0634', 'CVE-2016-0634', EXP_2016_0634),
    ('CVE-2014-7970', 'CVE-2014-7970', EXP_2014_7970),  # GH#211
    ('CVE-2016-7970', None, EXP_2016_7970),  # from NIST, not in RH
    ('CVE-2016-7543', 'CVE-2016-7543', EXP_2016_7543),
    ('CVE-2016-7076', 'CVE-2016-7076', EXP_2016_7076),  # GH#211, not in NIST, only in RH
    ('CVE-2018-1000156', 'CVE-2018-1000156', EXP_2018_1000156),
    ('CVE-9999-9999', None, None),
    ('', None, None)
]

# cve, number of responses, not grep
CVES_REGEX = [
    ('CVE-2018-1000', 1, 'CVE-2018-10000'),
    ('CVE-2018-1[0-9]{3}', 100, 'CVE-2018-1000001'),
    ('CVE-2017.*', 5000, None),
    ('CVE.*', 5000, None)
]


@pytest.mark.smoke
class TestCVEsQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple CVEs using POST."""
        request_body = tools.gen_cves_body([c[0] for c in CVES])
        cves = rest_api.get_cves(body=request_body).response_check()
        schemas.cves_schema.validate(cves.raw.body)
        expected_cves = [x for x in CVES if x not in CVES_NEG]
        assert len(cves) == len(expected_cves)
        for cve_name, _, _ in expected_cves:
            assert cve_name in cves

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_post_single(self, rest_api, cve_in):
        """Tests single CVE using POST."""
        cve_name, _, _ = cve_in
        if cve_name:
            request_body = tools.gen_cves_body([cve_name])
            cves = rest_api.get_cves(body=request_body).response_check()
        else:
            request_body = tools.gen_cves_body([])
            rest_api.get_cves(body=request_body).response_check(400)
            return

        if cve_name in [c[0] for c in CVES_NEG]:
            assert not cves
        else:
            schemas.cves_schema.validate(cves.raw.body)
            assert len(cves) == 1
            cve, = cves
            assert cve.name == cve_name

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_get(self, rest_api, cve_in):
        """Tests single CVE using GET."""
        cve_name, _, _ = cve_in
        if cve_name:
            cves = rest_api.get_cve(cve_name).response_check()
            if cve_name in [c[0] for c in CVES_NEG]:
                assert not cves
            else:
                schemas.cves_schema.validate(cves.raw.body)
                assert len(cves) == 1
                cve, = cves
                assert cve.name == cve_name
        else:
            rest_api.get_cve(cve_name).response_check(405)


@pytest.mark.smoke
@pytest.mark.skipif(GH(299).blocks, reason='Blocked by GH 299')
class TestCVEsModifiedSince(object):
    def test_post_multi(self, rest_api):
        """Tests multiple CVEs using POST."""
        request_body = tools.gen_cves_body(
            [c[0] for c in CVES], modified_since='2018-01-01T00:00:00+01:00')
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
            [cve_name], modified_since='2018-01-01T00:00:00+01:00')
        cves = rest_api.get_cves(body=request_body).response_check()
        # don't validate schema on empty response
        if expected_name:
            schemas.cves_schema.validate(cves.raw.body)
            assert len(cves) == 1
            cve, = cves
            assert cve.name == expected_name
        else:
            assert not cves

    @pytest.mark.parametrize('cve', ['CVE-2016-7076'])
    def test_modified_no_tz(self, rest_api, cve):
        """Tests modified since without timezone using POST."""
        request_body = tools.gen_cves_body(
            [cve], modified_since='2018-01-01T00:00:00')
        cves = rest_api.get_cves(body=request_body).response_check(400)
        assert 'Wrong date format' in cves.raw.body


@pytest.mark.smoke
@pytest.mark.skipif(GH(312).blocks, reason='Blocked by GH 312')
class TestCVEsCorrect(object):
    def test_post_multi(self, rest_api):
        """Tests multiple CVEs using POST."""
        request_body = tools.gen_cves_body([c[0] for c in CVES])
        cves = rest_api.get_cves(body=request_body).response_check()
        expected_cves = [x for x in CVES if x not in CVES_NEG]
        assert len(cves) == len(expected_cves)
        for cve_name, _, expected in expected_cves:
            cve = cves[cve_name]
            tools.validate_cves(cve, expected)

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_post_single(self, rest_api, cve_in):
        """Tests single CVE using POST."""
        cve_name, _, expected = cve_in
        if cve_name:
            request_body = tools.gen_cves_body([cve_name])
            cves = rest_api.get_cves(body=request_body).response_check()
        else:
            request_body = tools.gen_cves_body([])
            rest_api.get_cves(body=request_body).response_check(400)
            return

        if cve_name in [c[0] for c in CVES_NEG]:
            assert not cves
        else:
            assert len(cves) == 1
            cve, = cves
            tools.validate_cves(cve, expected)

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_get(self, rest_api, cve_in):
        """Tests single CVE using GET."""
        cve_name, _, expected = cve_in
        if not cve_name:
            rest_api.get_cve(cve_name).response_check(405)
        else:
            cves = rest_api.get_cve(cve_name).response_check()
            if cve_name in [c[0] for c in CVES_NEG]:
                assert not cves
            else:
                assert len(cves) == 1
                cve, = cves
                tools.validate_cves(cve, expected)


@pytest.mark.skipif(GH(311).blocks, reason='Blocked by GH 311')
@pytest.mark.smoke
class TestCVEsRegex(object):
    @pytest.mark.parametrize(
        'cve', CVES_REGEX, ids=[e[0] for e in CVES_REGEX])
    def test_post_single(self, rest_api, cve):
        """Tests single cve regex using POST."""
        cve_name, cve_num, not_grep = cve
        if cve_name in ['CVE-2017.*', 'CVE-2018-1[0-9]{3}', 'CVE.*'] and GH(320).blocks:
            pytest.skip("Blocked by GH#320")
        request_body = tools.gen_cves_body([cve_name])
        cve = rest_api.get_cves(body=request_body).response_check()
        schemas.cves_schema.validate(cve.raw.body)
        if cve_num == 1:
            assert len(cve) == 1
        else:
            assert len(cve) >= cve_num
        if not_grep:
            assert not not_grep in cve.raw

    @pytest.mark.parametrize(
        'cve', CVES_REGEX, ids=[e[0] for e in CVES_REGEX])
    def test_get(self, rest_api, cve):
        """Tests single cve regex using GET."""
        cve_name, cve_num, not_grep = cve
        if cve_name in ['CVE-2017.*', 'CVE-2018-1[0-9]{3}', 'CVE.*'] and GH(320).blocks:
            pytest.skip("Blocked by GH#320")
        cve = rest_api.get_cve(cve_name).response_check()
        schemas.cves_schema.validate(cve.raw.body)
        if cve_num == 1:
            assert len(cve) == 1
        else:
            assert len(cve) >= cve_num
        if not_grep:
            assert not not_grep in cve.raw
