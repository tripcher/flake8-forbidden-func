from __future__ import annotations

import dataclasses


@dataclasses.dataclass()
class Rule:
    rule: str
    comment: str
