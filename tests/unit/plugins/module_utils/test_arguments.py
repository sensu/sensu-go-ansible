from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments,
)


class TestGetSpec:
    @pytest.mark.parametrize("param", [
        "auth", "state", "name", "labels", "annotations",
    ])
    def test_valid_parameter(self, param):
        assert set(arguments.get_spec(param).keys()) == {param}

    def test_invalid_parameter(self):
        with pytest.raises(KeyError):
            arguments.get_spec("bad_parameter_name")

    def test_multiple_parameters(self):
        assert set(arguments.get_spec("auth", "name", "labels").keys()) == {
            "auth", "name", "labels",
        }


class TestGetSpecPayload:
    def test_no_key(self):
        params = dict(
            name="name",
            key="value"
        )

        assert arguments.get_spec_payload(params) == dict()

    def test_spec_payload(self):
        params = dict(
            name="name",
            key="value",
        )

        assert arguments.get_spec_payload(params, "key") == dict(
            key="value",
        )


class TestGetRenamedSpecPayload:
    def test_no_mapping(self):
        params = dict(
            name="name",
            key="value",
        )
        assert arguments.get_renamed_spec_payload(params, dict()) == dict()

    def test_renamed_payload(self):
        params = dict(
            name="name",
            key="value",
        )
        mapping = dict(
            name="new_name",
        )
        assert arguments.get_renamed_spec_payload(params, mapping) == dict(
            new_name="name",
        )


class TestGetMutationPayload:
    def test_name_only(self):
        params = dict(
            name="name",
        )

        assert arguments.get_mutation_payload(params) == dict(
            metadata=dict(
                name="name",
            ),
        )

    def test_name_and_namespace(self):
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
            key="value",
        )

        assert arguments.get_mutation_payload(params, "key") == dict(
            key="value",
            metadata=dict(
                name="name",
            ),
        )

    def test_namespace_is_none(self):
        params = dict(
            name="name",
            namespace=None,
        )

        with pytest.raises(AssertionError, match="BUG"):
            arguments.get_mutation_payload(params)

    def test_labels(self):
        params = dict(
            name="name",
            labels=dict(
                some="label",
                numeric=3,
            ),
        )

        assert arguments.get_mutation_payload(params) == dict(
            metadata=dict(
                name="name",
                labels=dict(
                    some="label",
                    numeric="3",
                ),
            ),
        )

    def test_annotations(self):
        params = dict(
            name="name",
            annotations=dict(
                my="Annotation",
                number=45,
            ),
        )

        assert arguments.get_mutation_payload(params) == dict(
            metadata=dict(
                name="name",
                annotations=dict(
                    my="Annotation",
                    number="45",
                ),
            ),
        )
