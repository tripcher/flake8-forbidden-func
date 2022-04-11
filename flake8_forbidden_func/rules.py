from __future__ import annotations

from flake8_forbidden_func.custom_types import Rule
from flake8_forbidden_func.pathes import convert_python_filepath_to_importable


def collect_all_forbidden_rules_for(
    *,
    filename: str,
    forbidden_rules: dict[str, list[Rule]] | None,
    allowed_rules: dict[str, list[Rule]] | None,
) -> set[Rule]:
    matching_rules = []
    verifiable_import = convert_python_filepath_to_importable(filename)

    if forbidden_rules:
        for import_rule, rules in forbidden_rules.items():
            if is_rule_matched(verifiable=verifiable_import, rule=import_rule):
                matching_rules += rules
    if allowed_rules:
        for import_rule, rules in allowed_rules.items():
            if not is_rule_matched(verifiable=verifiable_import, rule=import_rule):
                matching_rules += rules
    return set(matching_rules)


def is_rule_matched(*, verifiable: str, rule: str) -> bool:
    if '*' not in rule:
        match_result = verifiable == rule
    elif rule.startswith('*.') and rule.endswith('.*'):
        match_result = rule[1:-1] in verifiable
    elif rule.startswith('*.'):
        match_result = verifiable.endswith(rule[1:])
    elif rule.endswith('.*'):
        match_result = verifiable.startswith(rule[:-1])
    else:
        prefix, suffix = rule.split('*')
        match_result = verifiable.startswith(prefix) and verifiable.endswith(suffix)
    return match_result
