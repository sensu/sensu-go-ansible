# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json

from ansible.plugins.action import ActionBase
from ansible.utils.vars import merge_hash

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    bonsai, errors,
)


def validate_arguments(args):
    # TODO(@tadeboro): Add parameter type and presence validation here. Raise
    # errors.Error if validation should fail.
    pass


def build_asset_args(args):
    bonsai_args = bonsai.get_asset_parameters(args["name"], args["version"])
    asset_args = dict(
        name=args["name"],
        builds=bonsai_args["builds"],
    )

    # Only add optional parameter if it is present in at least one source.
    for meta in ("labels", "annotations"):
        if bonsai_args[meta] or args.get(meta):
            asset_args[meta] = merge_hash(
                bonsai_args[meta] or {}, args.get(meta, {}),
            )

    return asset_args


class ActionModule(ActionBase):

    TRANSFERS_FILES = False
    _VALID_ARGS = frozenset(("name", "version", "labels", "annotations"))

    def run(self, _tmp=None, task_vars=None):
        self._supports_check_mode = True
        self._supports_async = True

        result = super(ActionModule, self).run(task_vars)

        wrap_async = (
            self._task.async_val and not self._connection.has_native_async
        )

        try:
            validate_arguments(self._task.args)
            asset_args = build_asset_args(self._task.args)
            return merge_hash(
                result,
                self._execute_module(
                    module_name="sensu.sensu_go.asset", module_args=asset_args,
                    task_vars=task_vars, wrap_async=wrap_async,
                ),
            )
        except errors.Error as e:
            return dict(result, failed=True, msg=str(e))
        finally:
            if not wrap_async:
                self._remove_tmp_path(self._connection._shell.tmpdir)
