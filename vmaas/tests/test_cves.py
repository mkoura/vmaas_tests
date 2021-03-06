# -*- coding: utf-8 -*-

import pytest

from math import ceil
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

EXP_2018_1097 = [
    {
        "redhat_url": "https://access.redhat.com/security/cve/cve-2018-1097",
        "secondary_url": "https://bugzilla.redhat.com/show_bug.cgi?id=1561723",
        "synopsis": "CVE-2018-1097",
        "impact": "Moderate",
        "public_date": "2018-04-04T21:29:00+00:00",
        "cwe_list": [
            "CWE-200"
        ],
        "cvss3_score": "7.700"
    }
]

EXP_2002_2438 = [
    {
        "redhat_url": "",
        "secondary_url": "",
        "synopsis": "CVE-2002-2438",
        "impact": "NotSet",
        "public_date": "",
        "cwe_list": [],
        "cvss3_score": ""
    }
]

EXP_2017_7528 = [
    {
        "redhat_url": "",
        "secondary_url": "",
        "synopsis": "CVE-2017-7528",
        "impact": "Moderate",
        "public_date": "",
        "cwe_list": [
            "CWE-113"
        ],
        "cvss3_score": "5.200"
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
    ('CVE-2018-1097', 'CVE-2018-1097', EXP_2018_1097),  # Moderate impact from RH, High impact from NIST
    ('CVE-2017-7528', 'CVE-2017-7528', EXP_2017_7528),  # CVE has RESERVED status, with impact
    ('CVE-2002-2438', 'CVE-2002-2438', EXP_2002_2438),  # CVE has RESERVED status, without impact
    ('CVE-9999-9999', None, None),
    ('', None, None)
]

# cve, number of responses, not grep
CVES_REGEX = [
    ('CVE-2018-1000', 1, 'CVE-2018-10000'),
    ('CVE-2018-1[0-9]{3}', 100, 'CVE-2018-1000001'),
    ('CVE-2017.*', 5000, None),
    ('CVE.*', 5000, None),
    ('*', 0, None)
]

CVES_PAGE = ('CVE-2017-03.*', 99)

PAGE_SIZE = 40
DEFAULT_PAGE_SIZE = 5000
DEFAULT_PAGE = 1

PAGINATION_NEG = [
    ('page: 0', 0, DEFAULT_PAGE_SIZE),
    ('page: -2', -2, DEFAULT_PAGE_SIZE),
    ('page: 20', 20, DEFAULT_PAGE_SIZE),    # non existent page
    ('page: "string"', 'string', DEFAULT_PAGE_SIZE),
    ('page: nan', float('nan'), DEFAULT_PAGE_SIZE),
    ('page_size: 0', DEFAULT_PAGE, 0),
    ('page_size: -2', DEFAULT_PAGE, -2),
    ('page_size: "string"', DEFAULT_PAGE, 'string'),
    ('page_size: nan', DEFAULT_PAGE, float('nan')),
    ('page: 0, page_size: -2', DEFAULT_PAGE, DEFAULT_PAGE_SIZE),
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


@pytest.mark.skipif(GH(312).blocks, reason='Blocked by GH 312')
class TestCVEsCorrect(object):
    def post_multi(self, rest_api, rh_data_required=True):
        """Tests multiple CVEs using POST."""
        request_body = tools.gen_cves_body([c[0] for c in CVES])
        cves = rest_api.get_cves(body=request_body).response_check()
        expected_cves = [x for x in CVES if x not in CVES_NEG]
        assert len(cves) == len(expected_cves)
        for cve_name, _, expected in expected_cves:
            cve = cves[cve_name]
            tools.validate_cves(cve, expected, rh_data_required)

    def post_single(self, rest_api, cve_in, rh_data_required=True):
        """Tests single CVE using POST."""
        cve_name, __, expected = cve_in
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
            tools.validate_cves(cve, expected, rh_data_required)

    def get(self, rest_api, cve_in, rh_data_required=True):
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
                tools.validate_cves(cve, expected, rh_data_required)

    def test_post_multi(self, rest_api):
        """Tests multiple CVEs using POST."""
        self.post_multi(rest_api, rh_data_required=True)

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_post_single(self, rest_api, cve_in):
        """Tests single CVE using POST."""
        self.post_single(rest_api, cve_in, rh_data_required=True)

    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_get(self, rest_api, cve_in):
        """Tests single CVE using GET."""
        self.get(rest_api, cve_in, rh_data_required=True)

    @pytest.mark.smoke
    def test_post_multi_smoke(self, rest_api):
        """Tests multiple CVEs using POST."""
        self.post_multi(rest_api, rh_data_required=False)

    @pytest.mark.smoke
    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_post_single_smoke(self, rest_api, cve_in):
        """Tests single CVE using POST."""
        self.post_single(rest_api, cve_in, rh_data_required=False)

    @pytest.mark.smoke
    @pytest.mark.parametrize('cve_in', CVES, ids=[c[0] for c in CVES])
    def test_get_smoke(self, rest_api, cve_in):
        """Tests single CVE using GET."""
        self.get(rest_api, cve_in, rh_data_required=False)


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
        if cve_name == '*':
            rest_api.get_cves(body=request_body).response_check(400)
            return

        cve = rest_api.get_cves(body=request_body).response_check()
        schemas.cves_schema.validate(cve.raw.body)
        if cve_num == 1:
            assert len(cve) == 1
        else:
            assert len(cve) >= cve_num
        if not_grep:
            assert not_grep not in cve.raw

    @pytest.mark.parametrize(
        'cve', CVES_REGEX, ids=[e[0] for e in CVES_REGEX])
    def test_get(self, rest_api, cve):
        """Tests single cve regex using GET."""
        cve_name, cve_num, not_grep = cve
        if cve_name in ['CVE-2017.*', 'CVE-2018-1[0-9]{3}', 'CVE.*'] and GH(320).blocks:
            pytest.skip("Blocked by GH#320")
        if cve_name == '*':
            rest_api.get_cve(cve_name).response_check(400)
            return

        cve = rest_api.get_cve(cve_name).response_check()
        schemas.cves_schema.validate(cve.raw.body)
        if cve_num == 1:
            assert len(cve) == 1
        else:
            assert len(cve) >= cve_num
        if not_grep:
            assert not_grep not in cve.raw


class TestCVEsPagination(object):
    def test_pagination(self, rest_api):
        """Tests CVEs pagination using POST."""
        old_cves = []
        name, num = CVES_PAGE
        pages = ceil(num / PAGE_SIZE)
        for i in range(1, pages + 1):
            request_body = tools.gen_cves_body(
                cves=[name], page=i, page_size=PAGE_SIZE)
            cves = rest_api.get_cves(body=request_body).response_check()
            if i < pages:
                assert len(cves) == PAGE_SIZE
            else:
                # last page
                assert len(cves) == num % PAGE_SIZE

            schemas.cves_schema.validate(cves.raw.body)
            # Check if page/page_size/pages values are correct
            assert i == cves.raw.body['page']
            assert PAGE_SIZE == cves.raw.body['page_size']
            assert pages == cves.raw.body['pages']
            # erratum from old pages are not present on actual page
            for erratum in old_cves:
                assert erratum not in cves
            old_cves += cves

    @pytest.mark.parametrize('page_info', PAGINATION_NEG, ids=[i[0] for i in PAGINATION_NEG])
    def test_pagination_neg(self, rest_api, page_info):
        """Negative testing of CVEs pagination with page/page_size <= 0"""
        name, _ = CVES_PAGE
        _, page, page_size = page_info
        request_body = tools.gen_cves_body(cves=[name], page=page, page_size=page_size)
        if isinstance(page, str) or isinstance(page_size, str):
            rest_api.get_cves(body=request_body).response_check(400)
            return
        else:
            cves = rest_api.get_cves(body=request_body).response_check()

        assert DEFAULT_PAGE_SIZE == cves.raw.body['page_size']
        if page > DEFAULT_PAGE:
            assert page == cves.raw.body['page']
            assert not cves.raw.body['cve_list']
        else:
            assert DEFAULT_PAGE == cves.raw.body['page']
            assert cves
