"""
lsfiles.objects
===============
"""
import typing as _t
from collections.abc import MutableSequence as _MutableSequence


class MutableSequence(_MutableSequence):
    """Inherit to replicate subclassing of ``list`` objects."""

    def __init__(self) -> None:
        self._list: _t.List[_t.Any] = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._list}>"

    def __len__(self) -> int:
        return self._list.__len__()

    def __delitem__(self, key: _t.Any) -> None:
        self._list.__delitem__(key)

    def __setitem__(self, index: _t.Any, value: _t.Any) -> None:
        self._list.__setitem__(index, value)

    def __getitem__(self, index: _t.Any) -> _t.Any:
        return self._list.__getitem__(index)

    def insert(self, index: int, value: str) -> None:
        """Insert values into ``_list`` object.

        :param index: ``list`` index to insert ``value``.
        :param value: Value to insert into list.
        """
        if value not in self._list:
            self._list.insert(index, value)
