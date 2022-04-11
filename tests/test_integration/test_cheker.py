import ast

import pytest

from flake8_forbidden_func.custom_types import Rule
from flake8_forbidden_func.checker import FunctionChecker


_python_code = """
from bar import Model

faz = Model.objects.all().annotate().filter(a=2)
baz = bar_func()

if faz == baz:
    fuz = q.filter(a=1)
    return fuz.bar()
"""


@pytest.mark.parametrize(
    ('filename', 'expected_result'),
    [
        ('bar/another_test.py', []),
        (
            'test.py',
            [
                (4, 6, 'CFF001 *.filter call is forbidden, since comment error.', FunctionChecker),
                (5, 6, 'CFF001 bar_func call is forbidden, since comment error.', FunctionChecker),
                (8, 10, 'CFF001 *.filter call is forbidden, since comment error.', FunctionChecker),
                (4, 6, 'CFF001 Model.objects.all call is forbidden, since comment error.', FunctionChecker),
            ]
        ),
    ]
)
def test__function_checker__run__with_forbidden_functions(filename, expected_result):
    tree = ast.parse(_python_code)
    checker = FunctionChecker(filename=filename, tree=tree)
    checker.forbidden_functions = {
        'test': [
            Rule(rule='Model.objects.all', comment='comment error'),
            Rule(rule='*.filter', comment='comment error'),
            Rule(rule='bar_func', comment='comment error'),
        ],
        'test.bar': [
            Rule(rule='Model.objects.all', comment='comment error for bar'),
            Rule(rule='*.filter', comment='comment error for bar'),
            Rule(rule='bar_func', comment='comment error for bar'),
        ],
    }

    result = checker.run()

    assert list(result) == expected_result


@pytest.mark.parametrize(
    ('filename', 'expected_result'),
    [
        ('test.py', []),
        (
            'bar/another_test.py',
            [
                (4, 6, 'CFF001 *.filter call is forbidden, since comment error.', FunctionChecker),
                (5, 6, 'CFF001 bar_func call is forbidden, since comment error.', FunctionChecker),
                (8, 10, 'CFF001 *.filter call is forbidden, since comment error.', FunctionChecker),
                (4, 6, 'CFF001 Model.objects.all call is forbidden, since comment error.', FunctionChecker),
            ]
        ),
    ]
)
def test__function_checker__run__with_allowed_functions(filename, expected_result):
    tree = ast.parse(_python_code)
    checker = FunctionChecker(filename=filename, tree=tree)
    checker.allowed_functions = {
        'test': [
            Rule(rule='Model.objects.all', comment='comment error'),
            Rule(rule='*.filter', comment='comment error'),
            Rule(rule='bar_func', comment='comment error'),
        ]
    }

    result = checker.run()

    assert list(result) == expected_result


def test__function_checker__run__without_options():
    filename = 'test.py'
    tree = ast.parse(_python_code)
    checker = FunctionChecker(filename=filename, tree=tree)

    result = checker.run()

    assert list(result) == []
