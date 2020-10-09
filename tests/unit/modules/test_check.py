from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import check

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestDoSetsDiffer:
    @pytest.mark.parametrize("current,desired,diff", [
        ([1, 2, 3], [1, 2, 3], False),
        ([1, 2, 3], [3, 2, 1], False),
        ([1, 2], [1, 2, 3], True),
        ([1, 3], [2, 4], True),
    ])
    def test_comparison(self, current, desired, diff):
        c = dict(k=current)
        d = dict(k=desired)

        assert check.do_sets_differ(c, d, "k") is diff

    def test_missing_keys_are_treated_as_empty_sets(self):
        current = dict(a=[])
        desired = dict()

        assert check.do_sets_differ(current, desired, "a") is False
        assert check.do_sets_differ(desired, current, "a") is False

    def test_nulls_are_treated_as_empty_sets(self):
        current = dict(a=None)
        desired = dict(a=[])

        assert check.do_sets_differ(current, desired, "a") is False
        assert check.do_sets_differ(desired, current, "a") is False


class TestDoProxyRequestsDiffer:
    def test_missing_proxy_requests_in_desired_is_ignored(self):
        current = dict(proxy_requests=dict(entity_attributes=["a", "b"]))
        desired = dict()

        assert check.do_proxy_requests_differ(current, desired) is False

    @pytest.mark.parametrize("current,desired,diff", [
        (["a", "b"], ["a", "b"], False),
        (["a", "b"], ["b", "a"], False),
        (None, [], False),
        (["a", "b"], ["c", "a"], True),
        (["a", "b"], ["a", "b", "c"], True),
    ])
    def test_treat_entity_attributes_as_a_set(self, current, desired, diff):
        c = dict(proxy_requests=dict(entity_attributes=current))
        d = dict(proxy_requests=dict(entity_attributes=desired))

        assert check.do_proxy_requests_differ(c, d) is diff

    def test_ignore_missing_entity_attributes_in_desired(self):
        current = dict(proxy_requests=dict(entity_attributes=["a", "b"]))
        desired = dict(proxy_requests=dict())

        assert check.do_proxy_requests_differ(current, desired) is False

    @pytest.mark.parametrize("current,desired,diff", [
        (dict(splay=False), dict(splay=False), False),
        (dict(splay=False), dict(), False),
        (dict(splay=False), dict(splay=True), True),
        (dict(), dict(splay=True), True),
    ])
    def test_other_stuff_is_compared_as_usual(self, current, desired, diff):
        c = dict(proxy_requests=current)
        d = dict(proxy_requests=desired)

        assert check.do_proxy_requests_differ(c, d) is diff


class TestDoCheckHooksDiffer:
    def test_missing_check_hooks_in_desired_is_ignored(self):
        current = dict(check_hooks=[dict(warning=["a"])])
        desired = dict()

        assert check.do_check_hooks_differ(current, desired) is False

    @pytest.mark.parametrize("current,desired,diff", [
        (["a", "b"], ["a", "b"], False),
        (["a", "b"], ["b", "a"], False),
        (["a", "b"], ["c", "a"], True),
        (["a", "b"], ["a", "b", "c"], True),
    ])
    def test_treat_hooks_as_a_set(self, current, desired, diff):
        c = dict(check_hooks=[dict(warning=current)])
        d = dict(check_hooks=[dict(warning=desired)])

        assert check.do_check_hooks_differ(c, d) is diff


class TestDoDiffer:
    def test_no_difference(self):
        assert not check.do_differ(
            dict(
                command="sleep",
                subscriptions=["sub1", "sub2"],
                handlers=["ha1", "ha2", "ha3"],
                interval=123,
                cron="* * * 3 2",
                publish=False,
                timeout=30,
                ttl=60,
                stdin=True,
                low_flap_threshold=2,
                high_flap_threshold=10,
                runtime_assets=["asset1", "asset2"],
                check_hooks=[
                    dict(warning=["hook0-1", "hook0-2"]),
                    dict(critical=["hook1-1", "hook1-2"]),
                ],
                proxy_entity_name="name",
                proxy_requests=dict(
                    entity_attributes=["a1", "a2", "a3"],
                    splay=True,
                    splay_coverage=10,
                ),
                output_metric_format="influxdb_line",
                output_metric_handlers=["mhandler1", "mhandler2"],
                round_robin=False,
                env_vars=["k1=v1", "k2=v2"],
            ),
            dict(
                command="sleep",
                subscriptions=["sub2", "sub1"],
                handlers=["ha3", "ha1", "ha2"],
                interval=123,
                cron="* * * 3 2",
                publish=False,
                timeout=30,
                ttl=60,
                stdin=True,
                low_flap_threshold=2,
                high_flap_threshold=10,
                runtime_assets=["asset2", "asset1"],
                check_hooks=[
                    dict(critical=["hook1-2", "hook1-1"]),
                    dict(warning=["hook0-2", "hook0-1"]),
                ],
                proxy_entity_name="name",
                proxy_requests=dict(
                    splay=True,
                    entity_attributes=["a3", "a2", "a1"],
                    splay_coverage=10,
                ),
                output_metric_format="influxdb_line",
                output_metric_handlers=["mhandler2", "mhandler1"],
                round_robin=False,
                env_vars=["k2=v2", "k1=v1"],
            )
        )

    @pytest.mark.parametrize("current,desired", [
        (  # No diff in params, no secrets
            dict(name="demo"),
            dict(name="demo"),
        ),
        (  # No diff in params, no diff in secrets
            dict(name="demo", secrets=[
                dict(name="n1", secret="s1"), dict(name="n2", secret="s2"),
            ]),
            dict(name="demo", secrets=[
                dict(name="n2", secret="s2"), dict(name="n1", secret="s1"),
            ]),
        ),
    ])
    def test_no_difference_secrets(self, current, desired):
        assert check.do_differ(current, desired) is False

    @pytest.mark.parametrize("current,desired", [
        (  # Diff in params, no diff in secrets
            dict(name="demo", secrets=[dict(name="a", secret="1")]),
            dict(name="prod", secrets=[dict(name="a", secret="1")]),
        ),
        (  # No diff in params, missing and set secrets
            dict(name="demo", secrets=[dict(name="a", secret="1")]),
            dict(name="demo", secrets=[dict(name="b", secret="2")]),
        ),
        (  # Diff in params, missing and set secrets
            dict(name="demo", secrets=[dict(name="a", secret="1")]),
            dict(name="prod", secrets=[dict(name="b", secret="2")]),
        ),
    ])
    def test_difference_secrets(self, current, desired):
        assert check.do_differ(current, desired) is True


class TestSensuGoCheck(ModuleTestCase):
    def test_minimal_check_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name="test_check",
            command='echo "test"',
            subscriptions=['switches'],
            interval=60
        )

        with pytest.raises(AnsibleExitJson):
            check.main()

        state, _client, path, payload, check_mode, _d = sync_mock.call_args[0]
        assert state == "present"
        assert path == "/api/core/v2/namespaces/default/checks/test_check"
        assert payload == dict(
            command='echo "test"',
            subscriptions=['switches'],
            interval=60,
            metadata=dict(
                name="test_check",
                namespace="default",
            ),
        )
        assert check_mode is False

    def test_all_check_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_check',
            namespace='my',
            state='absent',
            command='/bin/true',
            subscriptions=['checks', 'also_checks'],
            handlers=['default', 'not_default'],
            interval=30,
            publish=True,
            timeout=30,
            ttl=100,
            stdin=False,
            low_flap_threshold=20,
            high_flap_threshold=60,
            proxy_entity_name='switch-dc-01',
            proxy_requests=dict(
                entity_attributes=['entity.entity_class == "proxy"'],
                splay=True,
                splay_coverage=90
            ),
            output_metric_format='nagios_perfdata',
            output_metric_handlers=['influx-db'],
            round_robin=True,
            env_vars=dict(foo='bar'),
            runtime_assets='awesomeness',
            secrets=[dict(name="a", secret="b")],
        )

        with pytest.raises(AnsibleExitJson):
            check.main()

        state, _client, path, payload, check_mode, _d = sync_mock.call_args[0]
        assert state == "absent"
        assert path == "/api/core/v2/namespaces/my/checks/test_check"
        assert payload == dict(
            command='/bin/true',
            subscriptions=['checks', 'also_checks'],
            interval=30,
            timeout=30,
            publish=True,
            handlers=['default', 'not_default'],
            env_vars=['foo=bar'],
            output_metric_handlers=['influx-db'],
            ttl=100,
            output_metric_format='nagios_perfdata',
            proxy_entity_name='switch-dc-01',
            proxy_requests=dict(entity_attributes=['entity.entity_class == "proxy"'],
                                splay=True,
                                splay_coverage=90),
            high_flap_threshold=60,
            low_flap_threshold=20,
            round_robin=True,
            stdin=False,
            runtime_assets=['awesomeness'],
            metadata=dict(
                name="test_check",
                namespace="my",
            ),
            secrets=[dict(name="a", secret="b")],
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.side_effect = errors.Error("Bad error")
        set_module_args(
            name='test_check',
            command='/bin/true',
            subscriptions=['checks', 'also_checks'],
            handlers=['default', 'not_default'],
            interval=30,
            publish=True,
            timeout=30,
            ttl=100,
            stdin=False,
            low_flap_threshold=20,
            high_flap_threshold=60,
            proxy_entity_name='switch-dc-01',
            proxy_requests=dict(
                entity_attributes=['entity.entity_class == "proxy"'],
                splay=True,
                splay_coverage=90
            ),
            output_metric_format='nagios_perfdata',
            output_metric_handlers=['influx-db'],
            round_robin=True,
            env_vars=dict(foo='bar'),
            runtime_assets='awesomeness'
        )

        with pytest.raises(AnsibleFailJson):
            check.main()
