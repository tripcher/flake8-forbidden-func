from typing import Generator, Tuple

from flake8_forbidden_func.__version__ import __version__ as version


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
        pass

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        if False:
            yield 1, 1, 'CFF001 error', type(self)
