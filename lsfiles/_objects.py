"""
lsfiles.objects
===============
"""
from __future__ import annotations

import typing as _t

T = _t.TypeVar("T")


class MutableSequence(_t.MutableSequence[T]):
    """Inherit to replicate subclassing of ``list`` objects."""

    def __init__(self) -> None:
        self._list: list[T] = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._list}>"

    def __len__(self) -> int:
        return self._list.__len__()

    @_t.overload
    def __delitem__(self, i: int) -> None:
        ...

    @_t.overload
    def __delitem__(self, i: slice) -> None:
        ...

    def __delitem__(self, i):
        return self._list.__delitem__(i)

    @_t.overload
    def __setitem__(self, i: int, o: T) -> None:
        ...

    @_t.overload
    def __setitem__(self, s: slice, o: _t.Iterable[T]) -> None:
        ...

    def __setitem__(self, i, o):
        return self._list.__setitem__(i, o)

    @_t.overload
    def __getitem__(self, i: int) -> T:
        ...

    @_t.overload
    def __getitem__(self, s: slice) -> _t.MutableSequence[T]:
        ...

    def __getitem__(self, i):
        return self._list.__getitem__(i)

    def insert(self, index: int, value: T) -> None:
        """Insert values into ``_list`` object.

        :param index: ``list`` index to insert ``value``.
        :param value: Value to insert into list.
        """
        if value not in self._list:
            self._list.insert(index, value)
