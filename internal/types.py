"""Typing"""

from typing import Literal, TypeAlias


number: TypeAlias = int | float # pylint: disable=invalid-name
AnchorEnum: TypeAlias = Literal['bottomleft', 'bottomright', 'topleft', 'topright']
Coords: TypeAlias = tuple[int, int]
Size: TypeAlias = tuple[int, int]
RGB: TypeAlias = tuple[int, int, int]
RGBA: TypeAlias = tuple[int, int, int, int]
Colors: TypeAlias = RGB | RGBA

__all__ = ['number', 'AnchorEnum', 'Coords', "RGB", "RGBA", "Colors"]
