# -*- coding: utf-8 -*-

import pytest

from math import ceil
from vmaas.rest import schemas, tools
from vmaas.utils.blockers import GH

ERRATA = [
    ('vmaas_test_1', None),
    ('vmaas_test_2', 'vmaas_test_2'),
]

ERRATA_NEG = [
    ('RHBA-2016:2858', None),
    ('RHEA-2010:0932', None),   # GH#310
    ('RHBA-2016:1031', None),   # GH#310
    ('RHSA-9999-9999', None),
    ('', None)
]

ERRATA_SMOKE = [
    ('RHBA-2016:2858', None),
    ('RHSA-2017:1931', None),
    ('RHSA-2018:1099', 'RHSA-2018:1099'),
    ('RHEA-2010:0932', None),   # GH#310
    ('RHBA-2016:1031', None),   # GH#310
    ('RHSA-9999-9999', None),
    ('', None)
]

ERRATA_REGEX = [
    ('vmaas', 0),
    ('vmaas.*', 9),
    ('RHSA-2018:\\d+', 44),
    ('RHSA-2018:015[1-5]', 1),
    ('RH.*', 573),      # GH#310
    ('*', 0)
]

ERRATA_PAGE = ('RHSA-2017.*', 141)

PAGE_SIZE = 50
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


class TestErrataQuery(object):
    def post_multi(self, rest_api, errata):
        """Tests multiple errata using POST."""
        request_body = tools.gen_errata_body([e[0] for e in errata])
        errata_response = rest_api.get_errata(
            body=request_body).response_check()
        schemas.errata_schema.validate(errata_response.raw.body)
        exp_errata = [x for x in errata if x not in ERRATA_NEG]
        assert len(errata_response) == len(exp_errata)
        for erratum_name, __ in exp_errata:
            assert erratum_name in errata_response

    def post_single(self, rest_api, erratum):
        """Tests single erratum using POST."""
        erratum_name, _ = erratum
        if erratum_name:
            request_body = tools.gen_errata_body([erratum_name])
            errata = rest_api.get_errata(body=request_body).response_check()
        else:
            request_body = tools.gen_errata_body([])
            rest_api.get_errata(body=request_body).response_check(400)
            return

        if erratum_name in [e[0] for e in ERRATA_NEG]:
            assert not errata
        else:
            schemas.errata_schema.validate(errata.raw.body)
            assert len(errata) == 1
            erratum, = errata
            assert erratum.name == erratum_name

    def test_post_multi(self, rest_api):
        """Tests multiple test errata using POST."""
        self.post_multi(rest_api, ERRATA)

    @pytest.mark.smoke
    @pytest.mark.skipif(GH(310).blocks, reason='Blocked by GH 310')
    def test_post_multi_smoke(self, rest_api):
        """Tests multiple real errata using POST."""
        self.post_multi(rest_api, ERRATA_SMOKE)

    @pytest.mark.parametrize('erratum', ERRATA, ids=[e[0] for e in ERRATA])
    def test_post_single(self, rest_api, erratum):
        """Tests single test erratum using POST."""
        self.post_single(rest_api, erratum)

    @pytest.mark.smoke
    @pytest.mark.parametrize('erratum', ERRATA_SMOKE, ids=[e[0] for e in ERRATA_SMOKE])
    def test_post_single_smoke(self, rest_api, erratum):
        """Tests single real erratum using POST."""
        if erratum[0] in ['RHEA-2010:0932', 'RHBA-2016:1031'] and GH(310).blocks:
            pytest.skip("Blocked by GH#310")
        self.post_single(rest_api, erratum)

    @pytest.mark.smoke
    @pytest.mark.parametrize('erratum', ERRATA_SMOKE, ids=[e[0] for e in ERRATA_SMOKE])
    def test_get(self, rest_api, erratum):
        """Tests single real erratum using GET."""
        erratum_name, _ = erratum
        if erratum_name in ['RHEA-2010:0932', 'RHBA-2016:1031'] and GH(310).blocks:
            pytest.skip("Blocked by GH#310")
        if not erratum_name:
            rest_api.get_erratum(erratum_name).response_check(405)
        else:
            errata = rest_api.get_erratum(erratum_name).response_check()
            if erratum_name in [e[0] for e in ERRATA_NEG]:
                assert not errata
            else:
                schemas.errata_schema.validate(errata.raw.body)
                assert len(errata) == 1
                erratum, = errata
                assert erratum.name == erratum_name


class TestErrataModifiedSince(object):
    def post_multi(self, rest_api, errata):
        """Tests multiple errata using POST."""
        request_body = tools.gen_errata_body(
            [e[0] for e in errata], modified_since='2018-04-06T00:00:00+01:00')
        errata_response = rest_api.get_errata(
            body=request_body).response_check()
        schemas.errata_schema.validate(errata_response.raw.body)
        assert len(errata_response) == len([e[1] for e in errata if e[1]])
        for __, expected_name in errata:
            if expected_name:  # not None
                assert expected_name in errata_response

    def post_single(self, rest_api, erratum):
        """Tests single erratum using POST."""
        name, expected_name = erratum
        if not name and GH(326).blocks:
            pytest.skip('Blocked by GH#326')
        request_body = tools.gen_errata_body(
            [name], modified_since='2018-04-06T00:00:00+01:00')
        errata = rest_api.get_errata(body=request_body).response_check()
        # don't validate schema on empty response
        if expected_name:
            schemas.errata_schema.validate(errata.raw.body)
            assert len(errata) == 1
            erratum, = errata
            assert erratum.name == expected_name
        else:
            assert not errata

    def test_post_multi(self, rest_api):
        """Tests multiple test errata using POST."""
        self.post_multi(rest_api, ERRATA)

    @pytest.mark.smoke
    def test_post_multi_smoke(self, rest_api):
        """Tests multiple real errata using POST."""
        self.post_multi(rest_api, ERRATA_SMOKE)

    @pytest.mark.parametrize('erratum', ERRATA, ids=[e[0] for e in ERRATA])
    def test_post_single(self, rest_api, erratum):
        """Tests single test erratum using POST."""
        self.post_single(rest_api, erratum)

    @pytest.mark.smoke
    @pytest.mark.parametrize('erratum', ERRATA_SMOKE, ids=[e[0] for e in ERRATA_SMOKE])
    def test_post_single_smoke(self, rest_api, erratum):
        """Tests single real erratum using POST."""
        self.post_single(rest_api, erratum)

    @pytest.mark.parametrize('erratum', ['RHBA-2016:2858'])
    def test_modified_no_tz(self, rest_api, erratum):
        """Tests modified since without timezone using POST."""
        request_body = tools.gen_errata_body(
            [erratum], modified_since='2018-04-06T00:00:00')
        errata = rest_api.get_errata(body=request_body).response_check(400)
        assert 'Wrong date format' in errata.raw.body


class TestErrataRegex(object):
    @pytest.mark.parametrize(
        'erratum', ERRATA_REGEX, ids=[e[0] for e in ERRATA_REGEX])
    def test_post_single(self, rest_api, erratum):
        """Tests single erratum using POST."""
        erratum_name, errata_num = erratum
        if erratum_name in ['RH.*'] and GH(310).blocks:
            pytest.skip("Blocked by GH#310")
        request_body = tools.gen_errata_body([erratum_name])
        if erratum_name == '*':
            errata = rest_api.get_errata(body=request_body).response_check(400)
        else:
            errata = rest_api.get_errata(body=request_body).response_check()
            assert len(errata) == errata_num
            if errata_num > 0:
                schemas.errata_schema.validate(errata.raw.body)

    @pytest.mark.parametrize(
        'erratum', ERRATA_REGEX, ids=[e[0] for e in ERRATA_REGEX])
    def test_get(self, rest_api, erratum):
        """Tests single real erratum using GET."""
        erratum_name, errata_num = erratum
        if erratum_name in ['RH.*'] and GH(310).blocks:
            pytest.skip("Blocked by GH#310")
        if erratum_name == '*':
            errata = rest_api.get_erratum(erratum_name).response_check(400)
        else:
            errata = rest_api.get_erratum(erratum_name).response_check()
            assert len(errata) == errata_num
            if errata_num > 0:
                schemas.errata_schema.validate(errata.raw.body)


class TestErrataPagination(object):
    def test_pagination(self, rest_api):
        """Tests errata pagination using POST."""
        old_errata = []
        name, num = ERRATA_PAGE
        pages = ceil(num / PAGE_SIZE)
        for i in range(1, pages + 1):
            request_body = tools.gen_errata_body(
                errata=[name], page=i, page_size=PAGE_SIZE)
            errata = rest_api.get_errata(body=request_body).response_check()
            if i < pages:
                assert len(errata) == PAGE_SIZE
            else:
                # last page
                assert len(errata) == num % PAGE_SIZE

            schemas.errata_schema.validate(errata.raw.body)
            # Check if page/page_size/pages values are correct
            assert i == errata.raw.body['page']
            assert PAGE_SIZE == errata.raw.body['page_size']
            assert pages == errata.raw.body['pages']
            # erratum from old pages are not present on actual page
            for erratum in old_errata:
                assert erratum not in errata
            old_errata += errata

    @pytest.mark.parametrize('page_info', PAGINATION_NEG, ids=[i[0] for i in PAGINATION_NEG])
    def test_pagination_neg(self, rest_api, page_info):
        """Negative testing of errata pagination with page/page_size <= 0"""
        name, _ = ERRATA_PAGE
        _, page, page_size = page_info
        request_body = tools.gen_errata_body(errata=[name], page=page, page_size=page_size)
        if isinstance(page, str) or isinstance(page_size, str):
            rest_api.get_errata(body=request_body).response_check(400)
            return
        else:
            errata = rest_api.get_errata(body=request_body).response_check()

        assert DEFAULT_PAGE_SIZE == errata.raw.body['page_size']
        if page > DEFAULT_PAGE:
            assert page == errata.raw.body['page']
            assert not errata.raw.body['errata_list']
        else:
            assert DEFAULT_PAGE == errata.raw.body['page']
            assert errata
