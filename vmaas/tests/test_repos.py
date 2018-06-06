# -*- coding: utf-8 -*-

import pytest

from vmaas.rest import schemas, tools
from vmaas.utils.blockers import GH

REPOS = [
    ('rhel-7-server-rpms', 1),
    ('vmaas-test-1', 1),
]

REPOS_NONEXISTENT = [
    'nonexistent-1',
    'nonexistent-2',
]


class TestReposQuery(object):
    def test_post_multi(self, rest_api):
        """Tests multiple repos using POST."""
        request_body = tools.gen_repos_body([p[0] for p in REPOS])
        repos = rest_api.get_repos(body=request_body).response_check()
        schemas.repos_schema.validate(repos.raw.body)
        assert len(repos) == len(REPOS)
        for repo_name, min_expected in REPOS:
            assert len(repos[repo_name]) >= min_expected

    @pytest.mark.parametrize('repo', REPOS, ids=[p[0] for p in REPOS])
    def test_post_single(self, rest_api, repo):
        """Tests single repo using POST."""
        repo_name, min_expected = repo
        request_body = tools.gen_repos_body([repo_name])
        repos = rest_api.get_repos(body=request_body).response_check()
        assert len(repos) == 1
        schemas.repos_schema.validate(repos.raw.body)
        repo, = repos
        assert len(repo) >= min_expected

    @pytest.mark.parametrize('repo', REPOS, ids=[p[0] for p in REPOS])
    def test_get(self, rest_api, repo):
        """Tests single repo using GET."""
        repo_name, min_expected = repo
        repos = rest_api.get_repo(repo_name).response_check()
        schemas.repos_schema.validate(repos.raw.body)
        assert len(repos) == 1
        repo, = repos
        assert len(repo) >= min_expected


class TestReposNonexistent(object):
    @pytest.mark.skipif(GH(299).blocks, reason='Blocked by GH 299')
    def test_post_multi(self, rest_api):
        """Tests multiple non-existent repos using POST."""
        request_body = tools.gen_repos_body(REPOS_NONEXISTENT)
        repos = rest_api.get_repos(body=request_body).response_check()
        assert len(repos) == len(REPOS_NONEXISTENT)
        for repo_name in REPOS_NONEXISTENT:
            assert not repos[repo_name]

    @pytest.mark.parametrize('repo_name', REPOS_NONEXISTENT)
    def test_post_single(self, rest_api, repo_name):
        """Tests single non-existent repo using POST."""
        request_body = tools.gen_repos_body([repo_name])
        repos = rest_api.get_repos(body=request_body).response_check()
        assert not repos

    @pytest.mark.parametrize('repo_name', REPOS_NONEXISTENT)
    def test_get(self, rest_api, repo_name):
        """Tests single non-existent repo using GET."""
        repos = rest_api.get_repo(repo_name).response_check()
        assert not repos
