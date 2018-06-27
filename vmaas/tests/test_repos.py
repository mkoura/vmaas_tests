# -*- coding: utf-8 -*-

import pytest

from math import ceil
from vmaas.rest import schemas, tools
from vmaas.utils.blockers import GH

REPOS = [
    ('vmaas-test-1', 1),
    ('vmaas-test-2', 1),
]

REPOS_SMOKE = [
    ('rhel-7-server-rpms', 1),
    ('rhel-7-workstation-rpms', 1),
]

REPOS_NONEXISTENT = [
    'nonexistent-1',
    'nonexistent-2',
    ''
]

REPOS_PAGE = ('vmaas.*', 5)

PAGE_SIZE = 3
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


class TestReposQuery(object):
    def post_multi(self, rest_api, repos):
        """Tests multiple repos using POST."""
        request_body = tools.gen_repos_body([p[0] for p in repos])
        repos_response = rest_api.get_repos(body=request_body).response_check()
        schemas.repos_schema.validate(repos_response.raw.body)
        assert len(repos_response) == len(repos)
        for repo_name, min_expected in repos:
            assert len(repos_response[repo_name]) >= min_expected

    def post_single(self, rest_api, repo):
        """Tests single repo using POST."""
        repo_name, min_expected = repo
        request_body = tools.gen_repos_body([repo_name])
        repos = rest_api.get_repos(body=request_body).response_check()
        assert len(repos) == 1
        schemas.repos_schema.validate(repos.raw.body)
        repo, = repos
        assert len(repo) >= min_expected

    def get(self, rest_api, repo):
        """Tests single repo using GET."""
        repo_name, min_expected = repo
        repos = rest_api.get_repo(repo_name).response_check()
        schemas.repos_schema.validate(repos.raw.body)
        assert len(repos) == 1
        repo, = repos
        assert len(repo) >= min_expected

    def test_post_multi(self, rest_api):
        """Tests multiple test repos using POST."""
        self.post_multi(rest_api, REPOS)

    @pytest.mark.smoke
    def test_post_multi_smoke(self, rest_api):
        """Tests multiple real repos using POST."""
        self.post_multi(rest_api, REPOS_SMOKE)

    @pytest.mark.parametrize('repo', REPOS, ids=[p[0] for p in REPOS])
    def test_post_single(self, rest_api, repo):
        """Tests single test repo using POST."""
        self.post_single(rest_api, repo)

    @pytest.mark.smoke
    @pytest.mark.parametrize('repo', REPOS_SMOKE, ids=[p[0] for p in REPOS_SMOKE])
    def test_post_single_smoke(self, rest_api, repo):
        """Tests single real repo using POST."""
        self.post_single(rest_api, repo)

    @pytest.mark.parametrize('repo', REPOS, ids=[p[0] for p in REPOS])
    def test_get(self, rest_api, repo):
        """Tests single test repo using GET."""
        self.get(rest_api, repo)

    @pytest.mark.smoke
    @pytest.mark.parametrize('repo', REPOS_SMOKE, ids=[p[0] for p in REPOS_SMOKE])
    def test_get_smoke(self, rest_api, repo):
        """Tests single real repo using GET."""
        self.get(rest_api, repo)


@pytest.mark.smoke
class TestReposNonexistent(object):
    @pytest.mark.skipif(GH(299).blocks, reason='Blocked by GH 299')
    @pytest.mark.skipif(GH(316).blocks, reason='Blocked by GH 316')
    def test_post_multi(self, rest_api):
        """Tests multiple non-existent repos using POST."""
        request_body = tools.gen_repos_body(REPOS_NONEXISTENT)
        repos = rest_api.get_repos(body=request_body).response_check()
        assert not repos

    @pytest.mark.parametrize('repo_name', REPOS_NONEXISTENT)
    def test_post_single(self, rest_api, repo_name):
        """Tests single non-existent repo using POST."""
        if repo_name:
            request_body = tools.gen_repos_body([repo_name])
            repos = rest_api.get_repos(body=request_body).response_check()
            assert not repos
        else:
            request_body = tools.gen_repos_body([])
            rest_api.get_repos(body=request_body).response_check(400)

    @pytest.mark.parametrize('repo_name', REPOS_NONEXISTENT)
    def test_get(self, rest_api, repo_name):
        """Tests single non-existent repo using GET."""
        if repo_name:
            repos = rest_api.get_repo(repo_name).response_check()
            assert not repos
        else:
            rest_api.get_repo(repo_name).response_check(405)


class TestReposPagination(object):
    def test_pagination(self, rest_api):
        """Tests repos pagination using POST."""
        old_repos = []
        name, num = REPOS_PAGE
        pages = ceil(num / PAGE_SIZE)
        for i in range(1, pages + 1):
            request_body = tools.gen_repos_body(
                repos=[name], page=i, page_size=PAGE_SIZE)
            repos = rest_api.get_repos(body=request_body).response_check()
            if i < pages:
                assert len(repos) == PAGE_SIZE
            else:
                # last page
                assert len(repos) == num % PAGE_SIZE

            schemas.repos_schema.validate(repos.raw.body)
            # Check if page/page_size/pages values are correct
            assert i == repos.raw.body['page']
            assert PAGE_SIZE == repos.raw.body['page_size']
            assert pages == repos.raw.body['pages']
            # erratum from old pages are not present on actual page
            for erratum in old_repos:
                assert erratum not in repos
            old_repos += repos

    @pytest.mark.parametrize('page_info', PAGINATION_NEG, ids=[i[0] for i in PAGINATION_NEG])
    def test_pagination_neg(self, rest_api, page_info):
        """Negative testing of repos pagination with page/page_size <= 0"""
        name, _ = REPOS_PAGE
        _, page, page_size = page_info
        request_body = tools.gen_repos_body(repos=[name], page=page, page_size=page_size)
        if isinstance(page, str) or isinstance(page_size, str):
            rest_api.get_repos(body=request_body).response_check(400)
            return
        else:
            repos = rest_api.get_repos(body=request_body).response_check()

        assert DEFAULT_PAGE_SIZE == repos.raw.body['page_size']
        if page > DEFAULT_PAGE:
            assert page == repos.raw.body['page']
            assert not repos.raw.body['repository_list']
        else:
            assert DEFAULT_PAGE == repos.raw.body['page']
            assert repos
