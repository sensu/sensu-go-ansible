#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: sensu_go_check
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu checks
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/checks/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.object
options:
  command:
    description:
      - Check command to run.
    required: true
  subscriptions:
    description:
      - List of subscriptions which receive check requests.
    type: list
    default: []
  handlers:
    description:
      - List of handlers which receive check results.
    type: list
    default: []
  interval:
    description:
      - Check request interval
    type: int
    default: 60
  cron:
    description:
      - Schedule check requests using crontab syntax
  publish:
    description:
      - Enables or disables scheduled publication of check requests.
    type: bool
    default: true
  timeout:
    description:
      - Check execution timeout
    type: int
    default: 30
  ttl:
    description:
      - Amount of time after which a check result is considered stale.
    type: int
  stdin:
    description:
      - Enables writing of serialized JSON data to the check command's stdin.
      - Only usable with checks written specifically for Sensu Go.
    type: bool
    default: false
  low_flap_threshold:
    description:
      - Low flap threshold.
    type: int
  high_flap_threshold:
    description:
      - High flap threshold.
  runtime_assets:
    description:
      - List of runtime assets required to run the check
    type: list
    default: []
  check_hooks:
    description:
      - A mapping of response codes to hooks which will be run by the agent when that code is returned.
    type: dict
  proxy_entity_name:
    description:
      - Entity name to associate this check with instead of the agent it ran on.
  proxy_entity_attributes:
    description:
      - List of attribute checks for determining which proxy entities this check should be scheduled against.
    type: list
  proxy_splay:
    description:
      - Enables or disables splaying of check request scheduling.
    type: bool
    default: false
  proxy_splay_coverage:
    description:
      - Percentage of the C(interval) over which to splay checks.
  output_metric_format:
    description:
      - Enable parsing of metrics in the specified format from this check's
        output.
    choices:
      - graphite_plaintext
      - influxdb_line
      - nagios_perfdata
      - opentsdb_line
  output_metric_handlers:
    description:
      - List of handlers which receive check results. I'm not sure why this exists.
    type: list
  env_vars:
    description:
      - A mapping of environment variable names and values to use with command execution.
    type: dict
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import SensuObject


class SensuCheck(SensuObject):
    def __init__(self, module):
        super(SensuCheck, self).__init__(module)

        self.path = '/checks/{0}'.format(self.params['name'])

        for key in (
            'command',
            'subscriptions',
            'handlers',
            'interval',
            'cron',
            'publish',
            'timeout',
            'ttl',
            'stdin',
            'low_flap_threshold',
            'high_flap_threshold',
            'runtime_assets',
            'proxy_entity_name',
            'output_metric_format',
            'output_metric_handlers',
        ):
            if self.params[key] is not None:
                self.payload[key] = self.params[key]

        self.param_dict_to_payload_list('check_hooks')
        self.param_dict_to_payload_kv_list('env_vars')

        if self.params['proxy_entity_attributes']:
            self.payload['proxy_requests'] = {
                'entity_attributes': self.params['proxy_entity_attributes'],
                'splay': self.params['proxy_splay'],
            }
            if self.params['proxy_splay']:
                self.payload['proxy']['splay_coverage'] = self.params['proxy_splay_coverage']


def main():
    argspec = SensuCheck.argument_spec()
    argspec.update(
        dict(
            command=dict(),
            subscriptions=dict(
                type='list',
            ),
            handlers=dict(
                type='list',
                default=[],
            ),
            interval=dict(
                type='int',
                default=60,
            ),
            cron=dict(),
            publish=dict(
                type='bool',
                default=True,
            ),
            timeout=dict(
                type='int',
                default=30,
            ),
            ttl=dict(
                type='int',
            ),
            stdin=dict(
                type='bool',
                default=False,
            ),
            env_vars=dict(
                type='dict',
            ),
            low_flap_threshold=dict(
                type='int',
            ),
            high_flap_threshold=dict(
                type='int',
            ),
            runtime_assets=dict(
                type='list',
            ),
            check_hooks=dict(
                type='dict',
            ),
            proxy_entity_name=dict(),
            proxy_entity_attributes=dict(
                type='list',
            ),
            proxy_splay=dict(
                type='bool',
                default=False,
            ),
            proxy_splay_coverage=dict(
                type='int',
                default=90,
            ),
            output_metric_format=dict(
                choices=['nagios_perfdata', 'graphite_plaintext', 'influxdb_line', 'opentsdb_line'],
            ),
            output_metric_handlers=dict(
                type='list',
            ),
        )
    )

    required_if = [('state', 'present', ['subscriptions', 'command'])]

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_if=required_if,
    )

    check = SensuCheck(module)
    result = check.reconcile()
    module.exit_json(changed=result['changed'], check=result['object'])


if __name__ == '__main__':
    main()
