from __future__ import annotations

from typing import Any

from dacite import from_dict
from django.db import connection


def convert_data_from_form_in_dacite(dto: Any, data: dict[str, Any]) -> Any:
    return from_dict(data_class=dto, data=data)


def parsing_create_unique_error_message(err: Exception) -> str:
    err_split = str(err).split(".")
    return err_split[-1]


def print_queries() -> None:
    print("============")
    queries_count = 0
    for i in connection.queries:
        print(i)
        queries_count += 1

    print(queries_count)
    print("============")
    return
