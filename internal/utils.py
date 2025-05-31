"""Utilities"""

from typing import Any, Type

class Temporary:
    def __init__(self, caller: Type[Any], attr_name: str, value: Any):
        self.temp = value
        self.attr_name = attr_name
        self.caller = caller
        self.orig = None

    def __enter__(self):
        self.orig = getattr(self.caller, self.attr_name)
        setattr(self.caller, self.attr_name, self.temp)
        return self

    def __exit__(self, *_):
        setattr(self.caller, self.attr_name, self.orig)
        return False
