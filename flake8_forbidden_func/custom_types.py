import dataclasses


@dataclasses.dataclass()
class Rule:
    rule: str
    comment: str
