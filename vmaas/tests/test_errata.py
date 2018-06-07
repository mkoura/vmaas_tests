# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import schemas, tools

ERRATA = [
    ('vmaas_test_1', None),
    ('vmaas_test_2', 'vmaas_test_2'),
]

ERRATA_SMOKE = [
    ('RHBA-2016:2858', None),
    ('RHSA-2017:1931', None),
    ('RHSA-2018:1099', 'RHSA-2018:1099')
]


class TestErrataQuery(object):
    def post_multi(self, rest_api, errata):
        """Tests multiple errata using POST."""
        request_body = tools.gen_errata_body([e[0] for e in errata])
        errata_response = rest_api.get_errata(body=request_body).response_check()
        schemas.errata_schema.validate(errata_response.raw.body)
        assert len(errata_response) == len(errata)
        for erratum_name, __ in errata:
            assert erratum_name in errata_response

    def post_single(self, rest_api, erratum):
        """Tests single erratum using POST."""
        erratum_name, _ = erratum
        request_body = tools.gen_errata_body([erratum_name])
        errata = rest_api.get_errata(body=request_body).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == 1
        erratum, = errata
        assert erratum.name == erratum_name

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

    @pytest.mark.smoke
    @pytest.mark.parametrize('erratum', ERRATA_SMOKE, ids=[e[0] for e in ERRATA_SMOKE])
    def test_get(self, rest_api, erratum):
        """Tests single real erratum using GET."""
        erratum_name, _ = erratum
        errata = rest_api.get_erratum(erratum_name).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == 1
        erratum, = errata
        assert erratum.name == erratum_name


class TestErrataModifiedSince(object):
    def post_multi(self, rest_api, errata):
        """Tests multiple errata using POST."""
        request_body = tools.gen_errata_body(
            [e[0] for e in errata], modified_since='2018-04-06')
        errata_response = rest_api.get_errata(body=request_body).response_check()
        schemas.errata_schema.validate(errata_response.raw.body)
        assert len(errata_response) == len([e[1] for e in errata if e[1]])
        for __, expected_name in errata:
            if expected_name:  # not None
                assert expected_name in errata_response

    def post_single(self, rest_api, erratum):
        """Tests single erratum using POST."""
        name, expected_name = erratum
        request_body = tools.gen_errata_body(
            [name], modified_since='2018-04-06')
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
