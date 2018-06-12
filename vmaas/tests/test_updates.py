# -*- coding: utf-8 -*-

import pytest

from vmaas.misc import packages
from vmaas.rest import schemas, tools
from vmaas.utils.blockers import GH


@pytest.mark.smoke
class TestUpdatesAll(object):
    def test_post_multi(self, rest_api):
        """Tests updates using POST with multiple packages."""
        request_body = tools.gen_updates_body(
            [p[0] for p in packages.PACKAGES])
        updates = rest_api.get_updates(body=request_body).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == len(packages.PACKAGES)
        for package_name, expected_updates in packages.PACKAGES:
            package = updates[package_name]
            tools.validate_package_updates(package, expected_updates)

    @pytest.mark.parametrize(
        'package_record', packages.PACKAGES, ids=[p[0] for p in packages.PACKAGES])
    def test_post_single(self, rest_api, package_record):
        """Tests updates using POST with single package."""
        name, expected_updates = package_record
        request_body = tools.gen_updates_body([name])
        updates = rest_api.get_updates(body=request_body).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected_updates)

    @pytest.mark.parametrize(
        'package_record', packages.PACKAGES, ids=[p[0] for p in packages.PACKAGES])
    def test_get(self, rest_api, package_record):
        """Tests updates using GET with single package."""
        name, expected_updates = package_record
        updates = rest_api.get_update(name).response_check()
        schemas.updates_top_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected_updates)


@pytest.mark.smoke
@pytest.mark.skipif(GH(301).blocks, reason='Blocked by GH 301')
class TestUpdatesInRepos(object):
    def test_post_multi(self, rest_api):
        """Tests updates in repos using POST with multiple packages."""
        request_body = tools.gen_updates_body(
            [p[0] for p in packages.PACKAGES_W_REPOS], repositories=packages.REPOS)
        updates = rest_api.get_updates(body=request_body).response_check()
        schemas.updates_top_repolist_schema.validate(updates.raw.body)
        assert len(updates) == len(packages.PACKAGES_W_REPOS)
        for package_name, expected_updates in packages.PACKAGES_W_REPOS:
            package = updates[package_name]
            tools.validate_package_updates(package, expected_updates)
            for update in package.available_updates:
                assert update['repository'] in packages.REPOS

    @pytest.mark.parametrize(
        'package_record', packages.PACKAGES_W_REPOS, ids=[p[0] for p in packages.PACKAGES_W_REPOS])
    def test_post_single(self, rest_api, package_record):
        """Tests updates in repos using POST with single package."""
        name, expected_updates = package_record
        request_body = tools.gen_updates_body(
            [name], repositories=packages.REPOS)
        updates = rest_api.get_updates(body=request_body).response_check()
        schemas.updates_top_repolist_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected_updates)
        for update in package.available_updates:
            assert update['repository'] in packages.REPOS

    @pytest.mark.skipif(GH(299).blocks, reason='Blocked by GH 299')
    def test_post_nonexistent_repo(self, rest_api):
        """Tests updates in repos using POST with single package."""
        name = packages.PACKAGES_W_REPOS[0][0]
        request_body = tools.gen_updates_body(
            [name], repositories=['nonexistent-1'])
        updates = rest_api.get_updates(body=request_body).response_check()
        assert not updates


@pytest.mark.skipif(GH(301).blocks, reason='Blocked by GH 301')
class TestUpdatesFilterRelease(object):
    def test_post_multi(self, rest_api):
        """Tests updates with filtered release version using POST with multiple packages."""
        request_body = tools.gen_updates_body(
            [p[0] for p in packages.PACKAGES_RELEASE_FILTER], releasever='6')
        updates = rest_api.get_updates(body=request_body).response_check()
        schemas.updates_top_releasever_schema.validate(updates.raw.body)
        assert len(updates) == len(packages.PACKAGES_RELEASE_FILTER)
        for package_name, expected_updates in packages.PACKAGES_RELEASE_FILTER:
            package = updates[package_name]
            tools.validate_package_updates(package, expected_updates)
            for update in package.available_updates:
                assert update['releasever'] == request_body['releasever']

    @pytest.mark.parametrize(
        'package_record',
        packages.PACKAGES_RELEASE_FILTER,
        ids=[p[0] for p in packages.PACKAGES_RELEASE_FILTER]
    )
    def test_post_single(self, rest_api, package_record):
        """Tests updates with filtered release version using POST with single package."""
        name, expected_updates = package_record
        request_body = tools.gen_updates_body([name], releasever='6')
        updates = rest_api.get_updates(body=request_body).response_check()
        schemas.updates_top_releasever_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected_updates)
        for update in package.available_updates:
            assert update['releasever'] == request_body['releasever']


@pytest.mark.skipif(GH(301).blocks, reason='Blocked by GH 301')
class TestUpdatesFilterBasearch(object):
    def test_post_multi(self, rest_api):
        """Tests updates with filtered basearch using POST with multiple packages."""
        request_body = tools.gen_updates_body(
            [p[0] for p in packages.PACKAGES_BASEARCH_FILTER], basearch='i386')
        updates = rest_api.get_updates(body=request_body).response_check()
        schemas.updates_top_basearch_schema.validate(updates.raw.body)
        assert len(updates) == len(packages.PACKAGES_BASEARCH_FILTER)
        for package_name, expected_updates in packages.PACKAGES_BASEARCH_FILTER:
            package = updates[package_name]
            tools.validate_package_updates(package, expected_updates)
            for update in package.available_updates:
                assert update['basearch'] == request_body['basearch']

    @pytest.mark.parametrize(
        'package_record',
        packages.PACKAGES_BASEARCH_FILTER,
        ids=[p[0] for p in packages.PACKAGES_BASEARCH_FILTER]
    )
    def test_post_single(self, rest_api, package_record):
        """Tests updates with filtered basearch using POST with single package."""
        name, expected_updates = package_record
        request_body = tools.gen_updates_body([name], basearch='i386')
        updates = rest_api.get_updates(body=request_body).response_check()
        schemas.updates_top_basearch_schema.validate(updates.raw.body)
        assert len(updates) == 1
        package, = updates
        tools.validate_package_updates(package, expected_updates)
        for update in package.available_updates:
            assert update['basearch'] == request_body['basearch']


class TestUpdatesDiff(object):
    def test_post_diff(self, make_conn):
        """Tests that application returns always the same response using POST."""
        request_body = tools.gen_updates_body(
            ['bash-0:4.2.46-20.el7_2.x86_64'])
        rest_api = make_conn()
        init = rest_api.get_updates(body=request_body).response_check()
        for i in range(100):
            rest_api = make_conn()
            response = rest_api.get_updates(body=request_body).response_check()
            assert init.raw.body == response.raw.body

    def test_get_diff(self, make_conn):
        """Tests that application returns always the same response using GET."""
        pkg = 'bash-0:4.2.46-20.el7_2.x86_64'
        rest_api = make_conn()
        init = rest_api.get_update(pkg).response_check()
        for i in range(100):
            rest_api = make_conn()
            response = rest_api.get_update(pkg).response_check()
            assert init.raw.body == response.raw.body
