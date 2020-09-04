#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import argparse
import json
import os
import sys

import yaml

from ansible.module_utils.urls import open_url


def _get_arg_parser():
    parser = argparse.ArgumentParser(description="Validate role metadata")
    parser.add_argument("role", nargs="+", help="role path")
    return parser


def _validate_role_platforms(platforms):
    url = "https://galaxy.ansible.com/api/v1/platforms/?name={0}&release={1}"

    msgs = []
    for platform in platforms:
        for release in platform["versions"]:
            resp = open_url(url.format(platform["name"], release))
            if len(json.loads(resp.read())["results"]) != 1:
                msgs.append(("ERROR", "Invalid platform '{0} {1}'".format(
                    platform["name"], release,
                )))

    return msgs


def _validate_role(role_path):
    meta_file = os.path.join(role_path, "meta", "main.yml")
    with open(meta_file) as fd:
        galaxy_info = yaml.safe_load(fd)["galaxy_info"]

    msgs = []
    msgs.extend(_validate_role_platforms(galaxy_info["platforms"]))

    return msgs


def main():
    args = _get_arg_parser().parse_args()
    no_msgs = 0
    for role in args.role:
        msgs = _validate_role(role)
        for msg in msgs:
            no_msgs += 1
            print("{0}: {1}".format(*msg))

    return 0 if no_msgs == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
