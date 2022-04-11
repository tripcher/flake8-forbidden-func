from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class Rule:
    rule: str
    comment: str


@dataclasses.dataclass(frozen=True)
class CallableNode:
    callable_str: str
    lineno: int
    col_offset: int
