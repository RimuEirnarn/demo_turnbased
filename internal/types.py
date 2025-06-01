"""Typing"""

from typing import Literal, TypeAlias


number: TypeAlias = int | float # pylint: disable=invalid-name
AnchorEnum: TypeAlias = Literal['bottomleft', 'bottomright', 'topleft', 'topright']

__all__ = ['number']
