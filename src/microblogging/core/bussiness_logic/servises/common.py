from __future__ import annotations

import sys
import uuid
from io import BytesIO
from typing import TYPE_CHECKING, Any

from dacite import from_dict
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import connection
from PIL import Image

if TYPE_CHECKING:
    from django.utils.datastructures import MultiValueDict


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
        print("-------")
        queries_count += 1

    print(queries_count)
    print("============")
    return None


def rename_in_uuid(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    file_extension = file.name.split(".")[-1]
    file_name = str(uuid.uuid4())
    file.name = file_name + "." + file_extension
    return file


def change_file_size(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    file_extension = file.content_type.split("/")[-1].upper()
    output = BytesIO()
    with Image.open(file) as image:
        image.thumbnail(size=(200, 150))
        image.save(fp=output, format=file_extension, quality=100)

    return InMemoryUploadedFile(
        file=output,
        field_name=file.field_name,
        name=file.name,
        content_type=file.content_type,
        size=sys.getsizeof(output),
        charset=file.charset,
    )


def change_photo(field: str, data: MultiValueDict) -> MultiValueDict:
    file = data[field]
    file = rename_in_uuid(file=file)
    file = change_file_size(file=file)
    data[field] = file
    return data
