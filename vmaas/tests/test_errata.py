# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import schemas, tools
from vmaas.utils.blockers import GH

ERRATA = [
    ('vmaas_test_1', None),
    ('vmaas_test_2', 'vmaas_test_2'),
]

ERRATA_NEG = [
    ('RHSA-9999-9999', None),
    ('', None)
]

ERRATA_SMOKE = [
    ('RHBA-2016:2858', None),
    ('RHSA-2017:1931', None),
    ('RHSA-2018:1099', 'RHSA-2018:1099'),
    ('RHEA-2010:0932', None),   # GH#310
    ('RHBA-2016:1031', None),    # GH#310
    ('RHSA-9999-9999', None),
    ('', None)
]

ERRATA_REGEX = [
    ('vmaas', 9),
    ('vmaas*', 9),
    ('RHSA-2018:\\d+', 44),
    ('RHSA-2018:015[1-5]', 1),
    ('RH.*', 5000)      # GH#310
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
        for erratum_name, __ in errata:
            assert erratum_name in errata_response

    def post_single(self, rest_api, erratum):
        """Tests single erratum using POST."""
        erratum_name, _ = erratum
        if not erratum_name:
            request_body = tools.gen_errata_body([])
        else:
            request_body = tools.gen_errata_body([erratum_name])
        errata = rest_api.get_errata(body=request_body).response_check()
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
    @pytest.mark.skipif(GH(310).blocks, reason='Blocked by GH 310')
    def test_post_multi(self, rest_api):
        """Tests multiple errata using POST."""
        request_body = tools.gen_errata_body([e[0] for e in ERRATA_REGEX])
        errata_response = rest_api.get_errata(
            body=request_body).response_check()
        schemas.errata_schema.validate(errata_response.raw.body)
        assert len(errata_response) == 5000  # default max responses per page

    @pytest.mark.parametrize(
        'erratum', ERRATA_REGEX, ids=[e[0] for e in ERRATA_REGEX])
    def test_post_single(self, rest_api, erratum):
        """Tests single erratum using POST."""
        erratum_name, errata_num = erratum
        if erratum_name in ['RH.*'] and GH(310).blocks:
            pytest.skip("Blocked by GH#310")
        request_body = tools.gen_errata_body([erratum_name])
        errata = rest_api.get_errata(body=request_body).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == errata_num

    @pytest.mark.parametrize(
        'erratum', ERRATA_REGEX, ids=[e[0] for e in ERRATA_REGEX])
    def test_get(self, rest_api, erratum):
        """Tests single real erratum using GET."""
        erratum_name, errata_num = erratum
        if erratum_name in ['RH.*'] and GH(310).blocks:
            pytest.skip("Blocked by GH#310")
        errata = rest_api.get_erratum(erratum_name).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == errata_num
