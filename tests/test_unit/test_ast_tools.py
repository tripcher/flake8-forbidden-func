from __future__ import annotations

import ast
import pytest

from flake8_forbidden_func.ast_tools import (
    convert_callable_to_callable_string,
    extract_callable_string_from
)
from flake8_forbidden_func.custom_types import CallableNode

_python_code = """
from bar import Model

faz = Model.objects.all().annotate().filter(a=2)
baz = bar_func()

if faz == baz:
    fuz = q.filter(a=1)
    return fuz.bar()
"""


def test__extract_callable_string_from():
    expected_result = [
        CallableNode(callable_str='Model.objects.all', lineno=4, col_offset=6),
        CallableNode(callable_str='Model.objects.annotate', lineno=4, col_offset=6),
        CallableNode(callable_str='fuz.bar', lineno=9, col_offset=11),
        CallableNode(callable_str='q.filter', lineno=8, col_offset=10),
        CallableNode(callable_str='Model.objects.filter', lineno=4, col_offset=6),
        CallableNode(callable_str='bar_func', lineno=5, col_offset=6)
    ]
    tree = ast.parse(_python_code)

    result = extract_callable_string_from(tree=tree)

    assert isinstance(result, list)
    assert set(result) == set(expected_result)
    assert len(result) == len(expected_result)


@pytest.mark.parametrize(
    ('code', 'expected_str'),
    [
        ('Model.objects.all()', 'Model.objects.all'),
        ('Model.objects.all().annotate()', 'Model.objects.annotate'),
        ('Model.objects.all().annotate().filter()', 'Model.objects.filter'),
        ('Model().bar()', 'Model.bar'),
        ('bur_func().bar_func().bar()', 'bur_func.bar_func.bar'),
        ('bur_func().bar_func()', 'bur_func.bar_func'),
        ('bur_func(t=1)', 'bur_func'),
        ('q.func()', 'q.func'),
        ('Model()', 'Model')
    ]
)
def test__convert_callable_to_callable_string(code, expected_str):
    tree = ast.parse(code)
    call = [n for n in ast.walk(tree) if isinstance(n, ast.Call)][0]

    result = convert_callable_to_callable_string(call=call)

    assert result == expected_str
