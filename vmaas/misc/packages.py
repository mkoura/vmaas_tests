EXPECTED_BASH = [
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:1931",
        "package": "bash-4.2.46-28.el7.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2014:1306",
        "package": "bash-4.2.45-5.el7_0.4.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:1931",
        "package": "bash-4.2.46-28.el7.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2014:1306",
        "package": "bash-4.2.45-5.el7_0.4.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    }
]

EXPECTED_VIM = [
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2016:2972",
        "package": "vim-common-2:7.4.160-1.el7_3.1.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2016:2972",
        "package": "vim-common-2:7.4.160-1.el7_3.1.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    },
]

EXPECTED_HTTPD = [
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2016:1422",
        "package": "httpd-2.4.6-40.el7_2.4.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:0906",
        "package": "httpd-2.4.6-45.el7_3.4.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:2479",
        "package": "httpd-2.4.6-67.el7_4.2.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:2882",
        "package": "httpd-2.4.6-67.el7_4.5.x86_64",
        "releasever": "7Server",
        "repository": "rhel-7-server-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2016:1422",
        "package": "httpd-2.4.6-40.el7_2.4.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:0906",
        "package": "httpd-2.4.6-45.el7_3.4.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:2479",
        "package": "httpd-2.4.6-67.el7_4.2.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    },
    {
        "basearch": "x86_64",
        "erratum": "RHSA-2017:2882",
        "package": "httpd-2.4.6-67.el7_4.5.x86_64",
        "releasever": "7Workstation",
        "repository": "rhel-7-workstation-rpms"
    }
]

EXPECTED_X86_64_TO_NOARCH = [
    {
        "basearch": "x86_64",
        "erratum": "vmaas_test_1",
        "package": "test-vmaas-0.3-3.noarch",
        "releasever": "7",
        "repository": "vmaas-test-1"
    }
]

EXPECTED_FROM_NOARCH = [
    {
        "basearch": "x86_64",
        "erratum": "vmaas_test_1",
        "package": "test-vmaas-0.3-3.noarch",
        "releasever": "7",
        "repository": "vmaas-test-1"
    }
]

EXPECTED_OTHER_REPO = [
    {
        "basearch": "x86_64",
        "erratum": "vmaas_test_2",
        "package": "test-vmaas-2-2.x86_64",
        "releasever": "7",
        "repository": "vmaas-test-2"
    }
]

EXPECTED_I386_FILTER_2_2 = [
    {
        "basearch": "x86_64",
        "erratum": "vmaas_test_i386_1.1",
        "package": "test-arch-vmaas-2-2.i386",
        "releasever": "7",
        "repository": "vmaas-test-x86_64"
    }
]

EXPECTED_I386_FILTER_3_3 = [
    {
        "basearch": "x86_64",
        "erratum": "vmaas_test_i386_2.1",
        "package": "test-arch-vmaas-3-3.i386",
        "releasever": "7",
        "repository": "vmaas-test-x86_64"
    }
]

EXPECTED_BASEARCH_FILTER_1 = [
    {
        "basearch": "i386",
        "erratum": "vmaas_test_i386_1",
        "package": "test-arch-vmaas-",
        "repository": "vmaas-test-i386"
    }
]

EXPECTED_BASEARCH_FILTER_2 = [
    {
        "basearch": "i386",
        "erratum": "vmaas_test_i386_2",
        "package": "test-arch-vmaas-",
        "repository": "vmaas-test-i386"
    }
]

EXPECTED_RELEASE_FILTER_1 = [
    {
        "erratum": "vmaas_test_i386_1",
        "package": "test-arch-vmaas-",
        "releasever": "6",
        "repository": "vmaas-test-i386"
    }
]

EXPECTED_RELEASE_FILTER_2 = [
    {
        "erratum": "vmaas_test_i386_2",
        "package": "test-arch-vmaas-",
        "releasever": "6",
        "repository": "vmaas-test-i386"
    }
]

# used for smoke tests
PACKAGES_BASIC = [
    # package, expected updates
    ('bash-0:4.2.45-5.el7_0.2.x86_64', EXPECTED_BASH),
    ('httpd-2.4.6-31.el7_1.1.x86_64', EXPECTED_HTTPD),
    ('vim-common-2:7.4.160-1.el7.x86_64', EXPECTED_VIM),
    ('vim-enhanced-2:7.4.160-2.el7.x86_64', None),
    ('telepathy-logger-0.8.0-5.el7.x86_64', None)
]

PACKAGES_TO_NOARCH = [
    # package, expected updates
    # update to noarch package expected
    ('test-vmaas-0.1-1.x86_64', EXPECTED_X86_64_TO_NOARCH + EXPECTED_OTHER_REPO),
    ('test-vmaas-0.2-2.x86_64', EXPECTED_X86_64_TO_NOARCH + EXPECTED_OTHER_REPO),
    ('test-vmaas-0.3-3.x86_64', EXPECTED_OTHER_REPO)
]

PACKAGES_FROM_NOARCH = [
    # package, expected updates
    # update from noarch to arch package expected
    ('test-vmaas-0.1-1.noarch', EXPECTED_FROM_NOARCH + EXPECTED_OTHER_REPO),
    ('test-vmaas-0.3-3.noarch', EXPECTED_OTHER_REPO)
]

PACKAGES_OTHER_REPO = [
    # package, expected updates
    # update to package from different repository within same product
    ('test-vmaas-0.1-1.x86_64', EXPECTED_X86_64_TO_NOARCH + EXPECTED_OTHER_REPO),
    ('test-vmaas-0.2-2.x86_64', EXPECTED_X86_64_TO_NOARCH + EXPECTED_OTHER_REPO),
    ('test-vmaas-0.3-3.x86_64', EXPECTED_OTHER_REPO),
    ('test-vmaas-1-1.x86_64', EXPECTED_OTHER_REPO),
    ('test-vmaas-2-2.x86_64', None),
    ('test-vmaas-3-3.x86_64', None)
]

PACKAGES_I386_W_FILTER = [
    ('test-arch-vmaas-1-1.i386', EXPECTED_I386_FILTER_2_2 + EXPECTED_I386_FILTER_3_3),
    ('test-arch-vmaas-2-2.i386', EXPECTED_I386_FILTER_3_3),
    ('test-arch-vmaas-3-3.i386', None)
]

PACKAGES_BASEARCH_FILTER = [
    ('test-arch-vmaas-1-1.i386', EXPECTED_BASEARCH_FILTER_1 + EXPECTED_BASEARCH_FILTER_2),
    ('test-arch-vmaas-2-2.i386', EXPECTED_BASEARCH_FILTER_2),
    ('test-arch-vmaas-3-3.i386', None)
]

PACKAGES_RELEASE_FILTER = [
    ('test-arch-vmaas-1-1.i386', EXPECTED_RELEASE_FILTER_1 + EXPECTED_RELEASE_FILTER_2),
    ('test-arch-vmaas-2-2.i386', EXPECTED_RELEASE_FILTER_2),
    ('test-arch-vmaas-3-3.i386', None)
]

EXPECTED_BASH_PARTIAL = [
    {
        "erratum": "RHSA-2017:1931",
        "repository": "rhel-7-server-rpms",
        "package": "bash-"
    },
    {
        "erratum": "RHSA-2017:1931",
        "repository": "rhel-7-workstation-rpms",
        "package": "bash-"
    },
]

EXPECTED_BASH_W_REPO = [
    {
        "erratum": "RHSA-2017:1931",
        "repository": "rhel-7-server-rpms",
        "package": "bash-"
    },
]

EXPECTED_POSTGRES = [
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-"
    },
]

EXPECTED_POSTGRES_W_REPO = [
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-"
    },
]

EXPECTED_POSTGRES_DEVEL = [
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-workstation-rpms",
        "package": "postgresql-devel-"
    }
]

EXPECTED_POSTGRES_DEVEL_W_REPO = [
    {
        "erratum": "RHSA-2017:1983",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:2728",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
    {
        "erratum": "RHSA-2017:3402",
        "repository": "rhel-7-server-rpms",
        "package": "postgresql-devel-"
    },
]


PACKAGES = [
    # package, expected updates
    ('bash-0:4.2.46-20.el7_2.x86_64', EXPECTED_BASH_PARTIAL),
    ('postgresql-0:9.2.18-1.el7.x86_64', EXPECTED_POSTGRES),
    ('postgresql-devel-9.2.18-1.el7.x86_64', EXPECTED_POSTGRES_DEVEL),
    ('telepathy-logger-0.8.0-5.el7.x86_64', None),
    ('vim-common-2:7.4.160-1.el7.x86_64.rpm', EXPECTED_VIM),
    ('bash-0:4.2.46-20.el7_2.i386', None),  # non existing A for given NEVR
    ('bash-0:9.2.18-1.el7.x86_64', None),  # non existing EVRA for given N
    ('bash-1', None),  # non existing NEVRA, N exists, wrong EVRA
    ('non-exist-0:1.1-1.el7.x86_64', None)
]

PACKAGES_W_REPOS = [
    # package, expected updates
    ('bash-0:4.2.46-20.el7_2.x86_64', EXPECTED_BASH_W_REPO),
    ('postgresql-0:9.2.18-1.el7.x86_64', EXPECTED_POSTGRES_W_REPO),
    ('postgresql-devel-9.2.18-1.el7.x86_64', EXPECTED_POSTGRES_DEVEL_W_REPO)
]

REPOS = [
    'vmaas-test-1',
    'rhel-7-server-rpms',
]

CACHED_PKG = 'bash-0:4.2.46-20.el7_2.x86_64'
