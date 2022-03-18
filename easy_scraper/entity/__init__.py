from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Elem:
    tag: str
    attrs: dict[str, str]
    children: list[Html]
    parent: Optional[Html]

    def __repr__(self) -> str:
        return f"<{self.tag} {self.attrs}>{ ' '.join(repr(c) for c in self.children) }</>"


@dataclass
class PlainText:
    data: str


@dataclass
class Pattern:
    name: str


class Empty:
    pass


Html = Union[Elem, PlainText, Pattern, Empty]
