"""
lsfiles._indexing
=================
"""
from __future__ import annotations

import re as _re
from pathlib import Path as _Path

import git as _git

from ._objects import MutableSequence as _MutableSequence


class LSFiles(_MutableSequence[_Path]):
    """Index all Python files in project."""

    def populate(self, exclude: str | None = None) -> None:
        """Populate object with index of versioned Python files.

        :param exclude: List of paths to exclude.
        """
        repo = _git.Repo(_Path.cwd())
        for path in repo.git.ls_files().splitlines():
            if path.endswith(".py") and (
                not exclude or _re.match(exclude, path) is None
            ):
                self.append(_Path.cwd() / path)

    def reduce(self) -> list[_Path]:
        """Get all relevant python files starting from project root.

        :return: List of project's Python file index, reduced to their
            root, relative to $PROJECT_DIR. Contains no duplicate items
            so $PROJECT_DIR/dir/file1.py and $PROJECT_DIR/dir/file2.py
            become $PROJECT_DIR/dir but PROJECT_DIR/file1.py and
            $PROJECT_DIR/file2.py remain as they are.
        """
        project_dir = _Path.cwd()
        return list(
            {project_dir / p.relative_to(project_dir).parts[0] for p in self}
        )

    def args(self, reduce: bool = False) -> tuple[str, ...]:
        """Return tuple suitable to be run with starred expression.

        :param reduce: :func:`~lsfiles.utils._Tree.reduce`
        :return: Tuple of `Path` objects or str repr.
        """
        paths = list(self)
        if reduce:
            paths = self.reduce()

        return tuple(str(p) for p in paths)
