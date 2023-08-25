from dataclasses import dataclass


@dataclass
class TwitsDTO:
    text: str
    tag: str
