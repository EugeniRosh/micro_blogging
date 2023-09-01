from __future__ import annotations

from typing import TYPE_CHECKING

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

if TYPE_CHECKING:
    from django.utils.safestring import SafeString

register = template.Library()


def escape_lambda(value: str) -> str:
    return value


@register.filter(needs_autoescape=True)
def text_link_filter(text: str, autoescape: bool = True) -> SafeString:
    text_split = text.split(" ")

    if autoescape:
        esc = conditional_escape
    else:
        esc = escape_lambda

    for i in range(len(text_split)):
        if "https://" in text_split[i] or "http://" in text_split[i]:
            link = esc(text_split[i])
            text_split[i] = f"<a href='{link}'>{link}</a>"

    result = " ".join(text_split)

    return mark_safe(result)
