# -*- coding: utf-8 -*-

# TODO: - pagination
#       e.g. I expect 4 repos are returned, set page_size=3,
#       first page contains 3 repos, 2nd page - 1 repo
#       same as for test_cves, test_errata

import pytest

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
        if not repo_name:
            request_body = tools.gen_repos_body([])
        else:
            request_body = tools.gen_repos_body([repo_name])
        repos = rest_api.get_repos(body=request_body).response_check()
        assert not repos

    @pytest.mark.parametrize('repo_name', REPOS_NONEXISTENT)
    def test_get(self, rest_api, repo_name):
        """Tests single non-existent repo using GET."""
        if not repo_name:
            rest_api.get_repo(repo_name).response_check(405)
        else:
            repos = rest_api.get_repo(repo_name).response_check()
            assert not repos
