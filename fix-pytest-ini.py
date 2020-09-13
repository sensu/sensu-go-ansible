#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os.path

from ansible_test._internal.util import ANSIBLE_TEST_DATA_ROOT


with open(os.path.join(ANSIBLE_TEST_DATA_ROOT, "pytest.ini")) as fd:
    lines = fd.readlines(True)

with open(os.path.join(ANSIBLE_TEST_DATA_ROOT, "pytest.ini"), "w") as fd:
    fd.writelines(line for line in lines if line.strip()[0] != "#")
