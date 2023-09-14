from dataclasses import dataclass
from typing import Iterable


@dataclass
class PaginationPageDTO:
    data: Iterable
    next_page: int | None
    prev_page: int | None
    navigation_num: Iterable
