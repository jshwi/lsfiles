"""
tests.conftest
==============
"""

from __future__ import annotations

import os
import typing as t
from configparser import ConfigParser
from pathlib import Path

import git
import pytest

from lsfiles import LSFiles

from . import FixtureMakeTree
from ._environ import GH_EMAIL, GH_NAME, REPO


@pytest.fixture(name="repo")
def fixture_repo(tmp_path: Path) -> git.Repo:
    """Get instantiated ``git.Repo`` object.

    :param tmp_path: Create and return temporary directory.
    :return: Instantiated ``git.Repo`` object.
    """
    return git.Repo.init(tmp_path / REPO)


@pytest.fixture(name="lsfiles")
def fixture_files() -> LSFiles:
    """Get instantiated ``LSFiles`` object.

    :return: Instantiated ``LSFiles`` object.
    """
    lsfiles = LSFiles()
    lsfiles.clear()
    lsfiles.populate()
    return lsfiles


@pytest.fixture(name="mock_environment", autouse=True)
def fixture_mock_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, repo: git.Repo
) -> None:
    """Mock imports to reflect the temporary testing environment.

    :param tmp_path: Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    :param repo: Instantiated ``git.Repo`` object.
    """
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr("os.getcwd", lambda: os.path.dirname(repo.git_dir))
    config = ConfigParser(default_section="")
    config.read_dict(
        {
            "user": {"name": GH_NAME, "email": GH_EMAIL},
            "advice": {"detachedHead": "false"},
            "init": {"defaultBranch": "master"},
        }
    )
    with open(Path.home() / ".gitconfig", "w", encoding="utf-8") as fout:
        config.write(fout)


@pytest.fixture(name="make_tree")
def fixture_make_tree() -> FixtureMakeTree:
    """Recursively create directory tree from dict mapping.

    :return: Function for using this fixture.
    """

    def _make_tree(root: Path, obj: dict[str, t.Any]) -> None:
        for key, value in obj.items():
            fullpath = root / key
            if isinstance(value, dict):
                fullpath.mkdir(exist_ok=True)
                _make_tree(fullpath, value)

            elif isinstance(value, str):
                os.symlink(value, fullpath)
            else:
                fullpath.touch()

    return _make_tree
