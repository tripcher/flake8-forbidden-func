from __future__ import annotations

from typing import Generator, Tuple

from flake8_forbidden_func.__version__ import __version__ as version
from flake8_forbidden_func.ast_tools import extract_callable_string_from
from flake8_forbidden_func.parser import parse_function_rules
from flake8_forbidden_func.rules import collect_all_forbidden_rules_for, is_rule_matched


class FunctionChecker:
    name = 'flake8-forbidden-func'
    version = version

    forbidden_functions = None
    allowed_functions = None

    def __init__(self, tree, filename: str):
        self.filename = filename
        self.tree = tree

    @classmethod
    def add_options(cls, parser) -> None:
        parser.add_option(
            '--forbidden-functions',
            default=None,
            parse_from_config=True,
        )
        parser.add_option(
            '--allowed-functions',
            default=None,
            parse_from_config=True,
        )

    @classmethod
    def parse_options(cls, options) -> None:
        if options.forbidden_functions:
            cls.forbidden_functions = parse_function_rules(
                raw_option_data=options.forbidden_functions
            )
        if options.allowed_functions:
            cls.allowed_functions = parse_function_rules(
                raw_option_data=options.allowed_functions
            )

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        if not self.forbidden_functions and not self.allowed_functions:
            return

        matching_forbidden_rules = collect_all_forbidden_rules_for(
            filename=self.filename,
            forbidden_rules=self.forbidden_functions,
            allowed_rules=self.allowed_functions
        )
        if matching_forbidden_rules:
            all_callable_nodes = extract_callable_string_from(tree=self.tree)
            for callable_node in all_callable_nodes:
                for rule in matching_forbidden_rules:
                    if is_rule_matched(verifiable=callable_node.callable_str, rule=rule.rule):
                        error_text = f'CFF001 {rule.rule} call is forbidden, since {rule.comment}.'
                        yield callable_node.lineno, callable_node.col_offset, error_text, type(self)
                        break
