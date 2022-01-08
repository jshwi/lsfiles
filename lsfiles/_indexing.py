"""
lsfiles._indexing
=================
"""
from __future__ import annotations

import typing as _t
from pathlib import Path as _Path

from gitspy import Git as _Git

from ._objects import MutableSequence as _MutableSequence

_git = _Git()


class LSFiles(_MutableSequence):
    """Index all Python files in project."""

    def __init__(self, exclude: _t.Optional[_t.List[str]] = None) -> None:
        super().__init__()
        self._exclude = exclude or []

    def add_exclusions(self, *exclusions: str) -> None:
        """Add iterable of str objects to exclude from indexing.

        :param exclusions: Iterable of str names to exclude from index.
        """
        self._exclude.extend(exclusions)

    def extend(self, values: _t.Iterable[_Path]) -> None:
        """Like extend for a regular list but cannot duplicate.

        :param values: Method expects an iterable of ``pathlib.Path``
            objects.
        """
        super().extend(values)
        self._list = list(set(self))

    def populate(self) -> None:
        """Populate object with index of versioned Python files."""
        _git.ls_files(capture=True)
        self.extend(
            _Path.cwd() / p
            for p in [_Path(p) for p in _git.stdout()]
            # exclude any basename, stem, or part of a
            # `pathlib.Path` path
            if not any(i in self._exclude for i in (*p.parts, p.stem))
            # only include Python files in index
            and p.name.endswith(".py")
        )

    def reduce(self) -> _t.List[_Path]:
        """Get all relevant python files starting from project root.

        :return: List of project's Python file index, reduced to their
            root, relative to $PROJECT_DIR. Contains no duplicate items
            so $PROJECT_DIR/dir/file1.py and $PROJECT_DIR/dir/file2.py
            become $PROJECT_DIR/dir but PROJECT_DIR/file1.py and
            $PROJECT_DIR/file2.py remain as they are.
        """
        project_dir = _Path.cwd()
        return list(
            set(
                project_dir / p.relative_to(project_dir).parts[0] for p in self
            )
        )

    def args(self, reduce: bool = False) -> _t.Tuple[str, ...]:
        """Return tuple suitable to be run with starred expression.

        :param reduce: :func:`~lsfiles.utils._Tree.reduce`
        :return: Tuple of `Path` objects or str repr.
        """
        paths = list(self)
        if reduce:
            paths = self.reduce()

        return tuple(str(p) for p in paths)
