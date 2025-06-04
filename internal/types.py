"""Typing"""

from typing import Literal, TypeAlias


number: TypeAlias = int | float # pylint: disable=invalid-name
AnchorEnum: TypeAlias = Literal['bottomleft', 'bottomright', 'topleft', 'topright']
RGB: TypeAlias = tuple[int, int, int]
RGBA: TypeAlias = tuple[int, int, int, int]
Colors: TypeAlias = RGB | RGBA

__all__ = ['number']
