#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Perf test for updates requests.
"""

import argparse
import collections
import json
import os
import random
import re
import subprocess
import sys

from contextlib import contextmanager
from xml.etree import ElementTree


TSUNG_XML = 'updates.xml'


Client = collections.namedtuple('Client', 'host cpus maxusers')
# cpus and maxusers are optional
Client.__new__.__defaults__ = (2, 600)

Server = collections.namedtuple('Server', 'host port')
# port defaults to 80
Server.__new__.__defaults__ = (80,)


# generate package lists

def load_package_list(packages_file):
    """Loads list of packages from file."""
    with open(packages_file) as pkgs:
        packages = pkgs.read().splitlines()
    return packages


def select_packages(packages, num):
    """Creates random list of packages."""
    return {random.choice(packages) for __ in range(num)}


def gen_packages_query(packages):
    """Generates request body for package updates query out of list of packages."""
    return dict(package_list=list(packages))


def gen_jsons(packages_file, counts_list):
    """Generates JSON files with updates requests."""
    jsons_list = []
    packages = load_package_list(packages_file)
    for i, count in enumerate(counts_list):
        selected = select_packages(packages, count)
        query = gen_packages_query(selected)
        json_file = 'updates{}.json'.format(i)
        with open(json_file, 'w') as out:
            json.dump(query, out, sort_keys=True, indent=4, separators=(',', ': '))
        jsons_list.append(json_file)

    return jsons_list


# generate tsung XML

def _top_element():
    """Creates top XML element."""
    top = ElementTree.Element('tsung', {'loglevel': 'warning'})
    return top


def _add_clients(parent_element, clients):
    """Adds clients section to XML."""
    client_element = ElementTree.SubElement(parent_element, 'clients')
    for host, cpu, maxusers in clients:
        attrs = {'host': host, 'cpu': str(cpu), 'maxusers': str(maxusers)}
        if host == 'localhost':
            attrs['use_controller_vm'] = 'true'
        ElementTree.SubElement(
            client_element,
            'client',
            attrs,
        )


def _add_servers(parent_element, servers):
    """Adds servers section to XML."""
    servers_element = ElementTree.SubElement(parent_element, 'servers')
    for host, port in servers:
        ElementTree.SubElement(
            servers_element,
            'server',
            {'host': host, 'port': str(port), 'type': 'tcp'}
        )


def _add_load(parent_element, duration, users, one_req_per_user=False):
    """Adds load section to XML."""
    load_element = ElementTree.SubElement(
        parent_element,
        'load',
        {'duration': str(duration), 'unit': 'second'}
    )
    phase_element = ElementTree.SubElement(
        load_element,
        'arrivalphase',
        {'phase': '1', 'duration': str(duration + 10), 'unit': 'second'}
    )

    users_data = {'arrivalrate': str(users), 'unit': 'second'}
    if not one_req_per_user:
        users_data['maxnumber'] = str(users)
    ElementTree.SubElement(phase_element, 'users', users_data)


def _add_sessions(parent_element, json_files, one_req_per_user=False):
    """Adds sessions section to XML."""
    sessions_element = ElementTree.SubElement(parent_element, 'sessions')
    for i, json_file in enumerate(json_files):
        session_element = ElementTree.SubElement(
            sessions_element,
            'session',
            {'type': 'ts_http', 'weight': '1', 'name': 'updates{}'.format(i)}
        )

        if one_req_per_user:
            requests_parent = session_element
        else:
            for_element = ElementTree.SubElement(
                session_element,
                'for',
                {'from': '1', 'to': '2', 'var': 'i', 'incr': '0'}
            )
            requests_parent = for_element

        request_element = ElementTree.SubElement(requests_parent, 'request')
        ElementTree.SubElement(
            request_element,
            'http',
            {
                'url': '/api/v1/updates/',
                'method': 'POST',
                'contents_from_file': json_file
            }
        )


def write_tsung_xml(xml_tree):
    """Writes tsung config."""
    with open(TSUNG_XML, 'wb') as tsung_config:
        tsung_config.write(
            '<?xml version="1.0" encoding="utf-8"?>'
            '<!DOCTYPE tsung SYSTEM "/usr/share/tsung/tsung-1.0.dtd" []>'.encode('utf8')
        )
        ElementTree.ElementTree(xml_tree).write(tsung_config, 'utf-8')


# pylint: disable=too-many-arguments
def gen_tsung_xml(
        packages_file, counts_list, clients, servers, duration, users_num, one_req_per_user):
    """Generates tsung config."""
    jsons_list = gen_jsons(packages_file, counts_list)
    top_element = _top_element()
    _add_clients(top_element, clients)
    _add_servers(top_element, servers)
    _add_load(top_element, duration, users_num, one_req_per_user)
    _add_sessions(top_element, jsons_list, one_req_per_user)
    write_tsung_xml(top_element)


def _get_objs_list(klass, data):
    objs_list = []
    if isinstance(data, str):
        data = [data]
    for rec in data:
        if ':' in rec:
            args = rec.split(':')
            objs_list.append(klass(*args))
        else:
            objs_list.append(klass(rec))
    return objs_list


def get_servers(servers):
    """Gets list of server data."""
    return _get_objs_list(Server, servers)


def get_clients(clients):
    """Gets list of clients data."""
    return _get_objs_list(Client, clients)


def get_counts_list(packages_num, requests_num):
    """Gets list of package numbers per request."""
    return [packages_num for __ in range(requests_num)]


@contextmanager
def _chdir(target_dir):
    original_dir = os.getcwd()
    os.chdir(target_dir)
    yield
    os.chdir(original_dir)


def gen_graphs(log_path):
    """Generates tsung graphs."""
    with _chdir(log_path):
        subprocess.run(
            ['tsung_stats', '--stats', 'tsung.log'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )


def run_tsung():
    """Runs tsung process."""
    ret = subprocess.run(
        ['tsung', '-f', TSUNG_XML, '-l', './', 'start'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

    log_path_re = re.search(r'Log directory is: (.*)', ret.stdout.decode('utf-8'))
    if not log_path_re:
        return 2

    log_path = log_path_re.group(1)
    gen_graphs(log_path)
    print('Log path: {}'.format(log_path))
    return 0


def get_args(args=None):
    """Gets command line arguments."""
    parser = argparse.ArgumentParser(description='run_upload_test')
    parser.add_argument('-i', '--packages_file', required=True,
                        help='File with list of rpm files')
    parser.add_argument('-s', '--server', required=True, action='append',
                        help='Server hostname:port')
    parser.add_argument('-c', '--client', default='localhost', action='append',
                        help='Client host:cpus:maxusers'
                             ' (default: %(default)s)')
    parser.add_argument('-d', '--duration', type=int, default=600, metavar='SEC',
                        help='Duration of test run (in seconds)'
                             ' (default: %(default)s)')
    parser.add_argument('-u', '--users_num', type=int, default=100, metavar='USERS',
                        help='How many concurrent users'
                             ' (default: %(default)s)')
    parser.add_argument('-p', '--packages_num', type=int, default=1000, metavar='PACKAGES',
                        help='How many packages per request'
                             ' (default: %(default)s)')
    parser.add_argument('--one-per-user', action='store_true',
                        help='Send just one request per user per second'
                             ' (default: %(default)s)')
    parser.add_argument('--requests-num', type=int, default=20, metavar='REQUESTS',
                        help='How many unique requests to generate'
                             ' (default: %(default)s)')
    return parser.parse_args(args)


def main(args=None):
    """Main function for cli."""
    args = get_args(args)
    gen_tsung_xml(
        args.packages_file,
        get_counts_list(args.packages_num, args.requests_num),
        get_clients(args.client),
        get_servers(args.server),
        args.duration,
        args.users_num,
        args.one_per_user,
    )
    return run_tsung()


if __name__ == '__main__':
    sys.exit(main())
