import pytest

from flake8_forbidden_func.custom_types import Rule
from flake8_forbidden_func.rules import collect_all_forbidden_rules_for


@pytest.fixture
def forbidden_rules():
    return {
        'a.*': [Rule(rule='a', comment='')],
        '*.bar': [Rule(rule='b', comment='')],
        '*.fuz.*': [Rule(rule='f', comment='')],
    }


@pytest.fixture
def allowed_rules():
    return {
        'allowed.bur.faz': [Rule(rule='allowed', comment='')],
    }


@pytest.mark.parametrize(
    ('filename', 'expected'),
    [
        ('a/foo.py', {Rule(rule='a', comment=''), Rule(rule='allowed', comment='')}),
        (
            'a/bar.py',
            {
                Rule(rule='a', comment=''),
                Rule(rule='b', comment=''),
                Rule(rule='allowed', comment='')
            }
        ),
        ('b/fuz/baz.py', {Rule(rule='f', comment=''), Rule(rule='allowed', comment='')}),
        ('b/bar/fuz/a/baz.py', {Rule(rule='f', comment=''), Rule(rule='allowed', comment='')}),
        (
            'a/fuz/bar.py',
            {
                Rule(rule='a', comment=''),
                Rule(rule='b', comment=''),
                Rule(rule='f', comment=''),
                Rule(rule='allowed', comment='')
            }
        ),
        ('b/baz.py', {Rule(rule='allowed', comment=''), }),
        ('b/bar/baz.py', {Rule(rule='allowed', comment='')}),
        ('allowed/bur/faz.py', set()),
    ],
)
def test__collect_forbidden_rules_for(filename, expected, forbidden_rules, allowed_rules):
    result = collect_all_forbidden_rules_for(
        filename=filename,
        forbidden_rules=forbidden_rules,
        allowed_rules=allowed_rules
    )

    assert result == expected
