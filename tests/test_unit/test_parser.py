from __future__ import annotations

import pytest

from flake8_forbidden_func.custom_types import Rule
from flake8_forbidden_func.parser import parse_function_rules


@pytest.mark.parametrize(
    ('raw_rules', 'expected_result'),
    [
        (
            (
                'foo.bar: *.annotate, error comment\n'
                '*.foo.bar.*: Model.object.*, error\n'
                'foo.bar: ModelClass, error 2\n'
            ),
            {
                'foo.bar': [
                    Rule(rule='*.annotate', comment='error comment'),
                    Rule(rule='ModelClass', comment='error 2'),
                ],
                '*.foo.bar.*': [Rule(rule='Model.object.*', comment='error')]
            }
        ),
        ('  *: Foo.bar, comment  ', {'*': [Rule(rule='Foo.bar', comment='comment')]})
    ]
)
def test__parse_function_rules(raw_rules, expected_result):
    result = parse_function_rules(raw_option_data=raw_rules)

    assert result == expected_result
