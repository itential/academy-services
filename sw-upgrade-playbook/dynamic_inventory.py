#!/usr/bin/env python3
"""
Dynamic Ansible inventory — translates IAG Inventory Manager node data into
Ansible inventory format.

Reads JSON (IAG inventory node data) from:
  1. stdin (if piped) — useful for local testing
  2. /tmp/ansible_inventory_cache.json — populated by IAG at runtime

Input shape:
  {"inventory_nodes": [{"name": "...", "attributes": {...}, "tags": [...]}]}

Node attributes are mapped to Ansible vars with this priority:
  ansible_* (native Ansible names, if present) → itential_* (IAG convention)
"""

import argparse
import json
import os
import sys

CACHE_FILE = '/tmp/ansible_inventory_cache.json'

# Itential/Netmiko platform → Ansible network_os
PLATFORM_TO_NETWORK_OS = {
    'cisco_ios': 'ios',
    'cisco_xr': 'iosxr',
    'ios': 'ios',
    'iosxr': 'iosxr',
    'nxos': 'nxos',
    'eos': 'eos',
    'junos': 'junos',
    'asa': 'asa',
    'aruba': 'arubaos',
    'bigip': 'bigip',
    'sros': 'sros',
}


def pick(attrs, *keys):
    """Return the first present value among keys, else None."""
    for k in keys:
        if k in attrs:
            return attrs[k]
    return None


def host_vars(attrs):
    """Map a node's attributes to Ansible host variables."""
    v = {}
    for ansible_key, itential_key in (
        ('ansible_host', 'itential_host'),
        ('ansible_user', 'itential_user'),
        ('ansible_password', 'itential_password'),
        ('ansible_port', 'itential_port'),
    ):
        value = pick(attrs, ansible_key, itential_key)
        if value is not None:
            v[ansible_key] = value

    # Derive ansible_network_os (and therefore network_cli connection)
    network_os = attrs.get('ansible_network_os')
    if not network_os:
        platform = attrs.get('itential_platform')
        if platform:
            network_os = PLATFORM_TO_NETWORK_OS.get(platform, platform)
    if network_os:
        v['ansible_network_os'] = network_os
        v['ansible_connection'] = attrs.get(
            'ansible_connection', 'ansible.netcommon.network_cli'
        )
    elif 'ansible_connection' in attrs:
        v['ansible_connection'] = attrs['ansible_connection']

    return v


def build_inventory(data):
    inv = {'_meta': {'hostvars': {}}, 'all': {'hosts': [], 'vars': {}}}
    for node in (data or {}).get('inventory_nodes', []):
        name = node.get('name')
        if not name:
            continue
        inv['all']['hosts'].append(name)
        inv['_meta']['hostvars'][name] = host_vars(node.get('attributes', {}))
        for tag in node.get('tags', []):
            inv.setdefault(tag, {'hosts': [], 'vars': {}})['hosts'].append(name)
    return inv


def load_data():
    """Return inventory data from stdin (if piped) or the cache file."""
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw:
            return json.loads(raw)
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return json.load(f)
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--list', action='store_true')
    p.add_argument('--host')
    args = p.parse_args()

    inv = build_inventory(load_data())

    if args.host:
        print(json.dumps(inv['_meta']['hostvars'].get(args.host, {})))
    else:
        print(json.dumps(inv))


if __name__ == '__main__':
    main()
