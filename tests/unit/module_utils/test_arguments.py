from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments,
)


class TestGetMutationPayload:
    def test_no_key(self):
        params = dict(
            name="name",
            namespace="space",
        )

        assert arguments.get_mutation_payload(params) == dict(
            metadata=dict(
                name="name",
                namespace="space",
            ),
        )

    def test_wanted_key(self):
        params = dict(
            name="name",
            namespace="space",
            key="value",
        )

        assert arguments.get_mutation_payload(params, "key") == dict(
            key="value",
            metadata=dict(
                name="name",
                namespace="space",
            ),
        )

    def test_labels(self):
        params = dict(
            name="name",
            namespace="space",
            labels=dict(
                some="label",
                numeric=3,
            ),
        )

        assert arguments.get_mutation_payload(params) == dict(
            metadata=dict(
                name="name",
                namespace="space",
                labels=dict(
                    some="label",
                    numeric="3",
                ),
            ),
        )

    def test_annotations(self):
        params = dict(
            name="name",
            namespace="space",
            annotations=dict(
                my="Annotation",
                number=45,
            ),
        )

        assert arguments.get_mutation_payload(params) == dict(
            metadata=dict(
                name="name",
                namespace="space",
                annotations=dict(
                    my="Annotation",
                    number="45",
                ),
            ),
        )
