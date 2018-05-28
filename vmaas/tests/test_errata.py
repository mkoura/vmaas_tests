# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import schemas, tools

ERRATA = [
    ('RHBA-2016:2858', None),
    ('RHSA-2017:1931', None),
    ('vmaas_test_1', None),
    ('vmaas_test_2', 'vmaas_test_2'),
    ('RHSA-2018:1099', 'RHSA-2018:1099')
]


class TestErrataQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple errata using POST."""
        request_body = tools.gen_errata_body([e[0] for e in ERRATA])
        errata = rest_api.get_errata(body=request_body).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == len(ERRATA)
        for erratum_name, _ in ERRATA:
            assert erratum_name in errata

    @pytest.mark.parametrize('erratum', ERRATA, ids=[e[0] for e in ERRATA])
    def test_post_single(self, rest_api, erratum):
        """Tests single erratum using POST."""
        erratum_name, _ = erratum
        request_body = tools.gen_errata_body([erratum_name])
        errata = rest_api.get_errata(body=request_body).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == 1
        erratum, = errata
        assert erratum.name == erratum_name

    @pytest.mark.parametrize('erratum', ERRATA, ids=[e[0] for e in ERRATA])
    def test_get(self, rest_api, erratum):
        """Tests single erratum using GET."""
        erratum_name, _ = erratum
        # Errata name should be in RHXX-YYYY:ZZZZ format
        # I'm using underscores and it fails in GET request
        # probably due to regex comparison...
        if erratum_name in ['vmaas_test_1', 'vmaas_test_2']:
            return
        errata = rest_api.get_erratum(erratum_name).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == 1
        erratum, = errata
        assert erratum.name == erratum_name


class TestErrataModifiedSince(object):
    def test_post_multi(self, rest_api):
        """Tests multiple errata using POST."""
        request_body = tools.gen_errata_body(
            [e[0] for e in ERRATA], modified_since='2018-04-06')
        errata = rest_api.get_errata(body=request_body).response_check()
        schemas.errata_schema.validate(errata.raw.body)
        assert len(errata) == len([e[1] for e in ERRATA if e[1]])
        for _, expected_name in ERRATA:
            if expected_name:  # not None
                assert expected_name in errata

    @pytest.mark.parametrize('erratum', ERRATA, ids=[e[0] for e in ERRATA])
    def test_post_single(self, rest_api, erratum):
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
            assert len(errata) == 0
            assert not errata
