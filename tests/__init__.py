"""
tests
=====

Test package for ``lsfiles``.
"""

import typing as t
from pathlib import Path

DIR = "dir"
DOTFILES = "dotfiles"
FILE_1 = "file1.py"
NESTED = "nested"
SRC = "src"
WHITELIST = "whitelist.py"

FixtureMakeTree = t.Callable[[Path, t.Dict[str, t.Any]], None]
