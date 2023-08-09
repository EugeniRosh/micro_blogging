from __future__ import annotations

from typing import Any

from dacite import from_dict


def convert_data_from_form_in_dacite(dto: Any, data: dict[str, Any]) -> Any:
    return from_dict(data_class=dto, data=data)


def parsing_create_unique_error_message(err: Exception) -> str:
    err_split = str(err).split(".")
    return err_split[-1]
