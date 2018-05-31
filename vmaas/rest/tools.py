# -*- coding: utf-8 -*-
"""
REST API helper functions
"""

import datetime

from vmaas.rest import schemas


def gen_cves_body(cves, modified_since=None):
    """Generates request body for CVEs query out of list of CVEs."""
    body = dict(cve_list=cves)
    if modified_since:
        if isinstance(modified_since, datetime.datetime):
            modified_since = modified_since.replace(microsecond=0).isoformat()
        body['modified_since'] = modified_since
    return body


def gen_errata_body(errata, modified_since=None):
    """Generates request body for errata query out of list of errata."""
    body = dict(errata_list=errata)
    if modified_since:
        if isinstance(modified_since, datetime.datetime):
            modified_since = modified_since.replace(microsecond=0).isoformat()
        body['modified_since'] = modified_since
    return body


def gen_repos_body(repos):
    """Generates request body for repos query out of list of repos."""
    return dict(repository_list=repos)


def gen_updates_body(
        packages, repositories=None, modified_since=None, basearch=None, releasever=None):
    """Generates request body for package updates query out of list of packages."""
    body = dict(package_list=packages)
    if repositories:
        body['repository_list'] = repositories
    if modified_since:
        if isinstance(modified_since, datetime.datetime):
            modified_since = modified_since.replace(microsecond=0).isoformat()
        body['modified_since'] = modified_since
    if basearch:
        body['basearch'] = basearch
    if releasever:
        body['releasever'] = releasever
    return body


def check_updates_uniq(updates):
    """Checks that returned update records are unique."""
    known_records = []
    not_unique = []
    for update in updates:
        for record in known_records:
            if record != update:
                continue
            # If we are here, the record is already known.
            # Making sure the record is added to `not_unique` list only once.
            for seen in not_unique:
                if seen == update:
                    break
            else:
                not_unique.append(record)
            break
        else:
            known_records.append(update)

    assert not not_unique, 'Duplicates found: {!r}'.format(not_unique)


def _updates_match(expected_update, available_update, exact_match):
    """Checks if expected update record matches available update record."""
    for key, value in expected_update.items():
        if key not in available_update:
            return False
        # partial match for package name
        if not exact_match:
            if key == 'package' and value in available_update[key]:
                continue
        # exact match for the rest of the values
        if value == available_update[key]:
            continue
        # if we are here, values don't match
        return False

    return True


def check_expected_updates(expected_updates, available_updates, exact_match):
    """Checks if all expected update records are present in available updates."""
    not_found = []
    for expected_update in expected_updates:
        for available_update in available_updates:
            if _updates_match(expected_update, available_update, exact_match):
                break
        else:
            not_found.append(expected_update)
    assert not not_found, 'Expected update not found: {!r}'.format(not_found)


def validate_package_updates(package, expected_updates, exact_match=False):
    """Runs checks on response body of 'updates' query."""
    if not package and not expected_updates:
        assert not package.get('description')
        assert not package.get('summary')
        return

    if (hasattr(package, 'available_updates') and not
            package.available_updates and not
            expected_updates):
        return

    if not package and expected_updates:
        assert False, 'Expected updates not present.\nPackage: {}\nExpected updates: {}'.format(
            package.raw, expected_updates)

    if not package.raw:
        # no point in checking schema etc.
        return

    # check package data using schema
    schemas.updates_package_schema.validate(package.raw)

    # check that available updates records are unique
    check_updates_uniq(package.available_updates)

    if not expected_updates:
        if exact_match:
            assert package.available_updates == []
        return

    # check that expected updates are present in the response
    if exact_match:
        assert len(package.available_updates) == len(expected_updates)
    else:
        assert len(package.available_updates) >= len(expected_updates)
    check_expected_updates(
        expected_updates, package.available_updates, exact_match)


def cve_match(expected, cve):
    """Checks if expected cve record matches cve record."""
    for key, value in expected.items():
        # exact match for all the values
        if value == cve[key]:
            continue
        # if we are here, values don't match
        return False

    return True


def validate_cves(cve, expected):
    """Runs checks on response body of 'cves' query."""

    if not cve and expected:
        assert False, 'Expected cves not present.\nCVE: {}\nExpected: {}'.format(
            cve.raw, expected)

    if not cve.raw:
        # no point in checking schema etc.
        return

    # check cve data using schema
    schemas.cves_data_schema.validate(cve.raw)

    # check that available updates records are unique
    check_updates_uniq(cve)

    # check that expected data are present in the response
    cve_match(expected[0], cve)
