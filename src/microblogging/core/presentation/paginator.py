from typing import Iterable

from core.bussiness_logic.dto import PaginationPageDTO
from core.bussiness_logic.exeptions import PaginationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class CustomPaginator:
    def __init__(self, max_value: int) -> None:
        self._max_value = max_value

    def paginate(self, data: Iterable, page_num: int) -> PaginationPageDTO:
        paginator = Paginator(object_list=data, per_page=self._max_value)

        try:
            data_paginator = paginator.page(number=page_num)
        except EmptyPage:
            raise PaginationError
        except PageNotAnInteger:
            raise PaginationError

        paginator_navigator = paginator.get_elided_page_range(page_num)

        if data_paginator.has_next():
            next_page_num = data_paginator.next_page_number()
        else:
            next_page_num = None

        if data_paginator.has_previous():
            prev_page_num = data_paginator.previous_page_number()
        else:
            prev_page_num = None

        return PaginationPageDTO(
            data=data_paginator,
            next_page=next_page_num,
            prev_page=prev_page_num,
            navigation_num=paginator_navigator,
        )
