from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import sys


def _load_scenario_weights(source):
    scenarios = []
    with open(source) as fd:
        for line in fd:
            name, weight = line.strip().split()
            scenarios.append((float(weight), name))

    return sorted(scenarios, reverse=True)


def _partition_scenarios(scenarios, n_partitions):
    # We need idx field in partition in order to make partitioning algorithm
    # deterministic - we use it to break ties when two or more partitions have
    # the same weight.
    partitions = tuple(
        dict(idx=i, weight=0.0, scenarios=[]) for i in range(n_partitions)
    )
    top = partitions[0]

    for weight, name in scenarios:
        top["weight"] += weight
        top["scenarios"].append(name)
        top = min(partitions, key=lambda x: (x["weight"], x["idx"]))

    return partitions


def main(source, partition_idx, n_partitions):
    scenarios = _load_scenario_weights(source)
    partitions = _partition_scenarios(scenarios, n_partitions)
    print(" ".join(partitions[partition_idx]["scenarios"]))


if __name__ == "__main__":
    main(
        sys.argv[1],
        int(os.environ["CIRCLE_NODE_INDEX"]),
        int(os.environ["CIRCLE_NODE_TOTAL"]),
    )
