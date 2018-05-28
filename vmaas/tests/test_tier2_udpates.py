# -*- coding: utf-8 -*-

import pytest

from vmaas.misc import packages
from vmaas.rest import schemas, tools


class TestUpdatesBasic(object):
    def test_post_multi(self, rest_api):
        """Tests correct updates using POST with multiple packages."""
        body = tools.gen_updates_body([p[0] for p in packages.PACKAGES_BASIC])
        updates = rest_api.get_updates(body=body).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == len(packages.PACKAGES_BASIC)
        for name, expected in packages.PACKAGES_BASIC:
            tools.validate_package_updates(
                updates[name], expected, exact_match=True)

    @pytest.mark.parametrize(
        'package', packages.PACKAGES_BASIC, ids=[p[0] for p in packages.PACKAGES_BASIC])
    def test_post_single(self, rest_api, package):
        """Tests correct updates using POST with single package."""
        name, expected = package
        body = tools.gen_updates_body([name])
        updates = rest_api.get_updates(body=body).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected, exact_match=True)

    @pytest.mark.parametrize(
        'package', packages.PACKAGES_BASIC, ids=[p[0] for p in packages.PACKAGES_BASIC])
    def test_get_single(self, rest_api, package):
        """Tests correct updates using GET with single package."""
        name, expected = package
        updates = rest_api.get_update(name).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected, exact_match=True)


class TestUpdateInOtherRepo(object):
    def test_post_multi(self, rest_api):
        """Tests correct updates in different repo using POST with multiple packages."""
        body = tools.gen_updates_body(
            [p[0] for p in packages.PACKAGES_OTHER_REPO])
        updates = rest_api.get_updates(body=body).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == len(packages.PACKAGES_OTHER_REPO)
        for name, expected in packages.PACKAGES_OTHER_REPO:
            tools.validate_package_updates(
                updates[name], expected, exact_match=True)

    @pytest.mark.parametrize(
        'package', packages.PACKAGES_OTHER_REPO, ids=[p[0] for p in packages.PACKAGES_OTHER_REPO])
    def test_post_single(self, rest_api, package):
        """Tests correct updates in different repo using POST with single package."""
        name, expected = package
        body = tools.gen_updates_body([name])
        updates = rest_api.get_updates(body=body).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected, exact_match=True)

    @pytest.mark.parametrize(
        'package', packages.PACKAGES_OTHER_REPO, ids=[p[0] for p in packages.PACKAGES_OTHER_REPO])
    def test_get_single(self, rest_api, package):
        """Tests correct updates in different repo using GET with single package."""
        name, expected = package
        updates = rest_api.get_update(name).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected, exact_match=True)


class TestUpdateToNoarch(object):
    def test_post_multi(self, rest_api):
        """Tests correct updates to noarch package using POST with multiple packages."""
        body = tools.gen_updates_body(
            [p[0] for p in packages.PACKAGES_TO_NOARCH])
        updates = rest_api.get_updates(body=body).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == len(packages.PACKAGES_TO_NOARCH)
        for name, expected in packages.PACKAGES_TO_NOARCH:
            tools.validate_package_updates(updates[name], expected,
                                           exact_match=True)

    @pytest.mark.parametrize(
        'package', packages.PACKAGES_TO_NOARCH, ids=[p[0] for p in packages.PACKAGES_TO_NOARCH])
    def test_post_single(self, rest_api, package):
        """Tests correct updates to noarch package using POST with single package."""
        name, expected = package
        body = tools.gen_updates_body([name])
        updates = rest_api.get_updates(body=body).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected, exact_match=True)

    @pytest.mark.parametrize(
        'package', packages.PACKAGES_TO_NOARCH, ids=[p[0] for p in packages.PACKAGES_TO_NOARCH])
    def test_get_single(self, rest_api, package):
        """Tests correct updates to noarch package using GET with single package."""
        name, expected = package
        updates = rest_api.get_update(name).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected, exact_match=True)


class TestUpdateFromNoarch(object):
    def test_post_multi(self, rest_api):
        """Tests correct updates from noarch using POST with multiple packages."""
        body = tools.gen_updates_body(
            [p[0] for p in packages.PACKAGES_FROM_NOARCH])
        updates = rest_api.get_updates(body=body).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == len(packages.PACKAGES_FROM_NOARCH)
        for name, expected in packages.PACKAGES_FROM_NOARCH:
            tools.validate_package_updates(
                updates[name], expected, exact_match=True)

    @pytest.mark.parametrize(
        'package', packages.PACKAGES_FROM_NOARCH, ids=[p[0] for p in packages.PACKAGES_FROM_NOARCH])
    def test_post_single(self, rest_api, package):
        """Tests correct updates from noarch using POST with single package."""
        name, expected = package
        body = tools.gen_updates_body([name])
        updates = rest_api.get_updates(body=body).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected, exact_match=True)

    @pytest.mark.parametrize(
        'package', packages.PACKAGES_FROM_NOARCH, ids=[p[0] for p in packages.PACKAGES_FROM_NOARCH])
    def test_get_single(self, rest_api, package):
        """Tests correct updates from noarch using GET with single package."""
        name, expected = package
        updates = rest_api.get_update(name).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected, exact_match=True)


class TestUpdateI386Filter(object):
    def test_post_multi(self, rest_api):
        """Tests correct updates from i386 package with basearch set to x86_64
        using POST with multiple packages.
        """
        body = tools.gen_updates_body(
            [p[0] for p in packages.PACKAGES_I386_W_FILTER], basearch='x86_64')
        updates = rest_api.get_updates(body=body).response_check()
        schemas.updates_top_basearch_schema.validate(updates.raw.body)
        assert len(updates) == len(packages.PACKAGES_I386_W_FILTER)
        for name, expected in packages.PACKAGES_I386_W_FILTER:
            tools.validate_package_updates(
                updates[name], expected, exact_match=True)

    @pytest.mark.parametrize(
        'package',
        packages.PACKAGES_I386_W_FILTER,
        ids=[p[0] for p in packages.PACKAGES_I386_W_FILTER]
    )
    def test_post_single(self, rest_api, package):
        """Tests correct updates from i386 package with basearch set to x86_64
        using POST with single package.
        """
        name, expected = package
        body = tools.gen_updates_body([name], basearch='x86_64')
        updates = rest_api.get_updates(body=body).response_check()
        schemas.updates_top_basearch_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected, exact_match=True)
