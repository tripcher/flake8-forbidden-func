from __future__ import annotations

from flake8_forbidden_func.checker import FunctionChecker


def test__function_checker__check_name():
    assert FunctionChecker.name == 'flake8-forbidden-func'
