from __future__ import annotations

import collections

from flake8_forbidden_func.custom_types import Rule


def parse_function_rules(*, raw_option_data: str) -> dict[str, list[Rule]]:
    lines = raw_option_data.strip().split('\n')
    parsed_option = collections.defaultdict(list)
    for line in lines:
        imports_from, raw_rules = line.split(': ')
        rule, comment = raw_rules.split(', ')
        for import_from in imports_from.split(', '):
            parsed_option[import_from.strip()].append(
                Rule(rule=rule, comment=comment),
            )
    return dict(parsed_option)
