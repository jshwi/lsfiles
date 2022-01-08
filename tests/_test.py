"""
tests._test
===========
"""
import typing as t
from pathlib import Path

import pytest
from gitspy import Git

from lsfiles import LSFiles

from ._environ import FILES, GITIGNORE, INIT, REPO, WHITELIST_PY


@pytest.mark.parametrize(
    "make_relative_file,assert_relative_item,assert_true",
    [
        (FILES, FILES, True),
        (Path("nested") / "python" / "file" / FILES, "nested", True),
        (WHITELIST_PY, "whitelist.py", False),
    ],
    ids=["file", "nested", "exclude"],
)
def test_get_files(
    git: Git,
    lsfiles: LSFiles,
    make_relative_file: str,
    assert_relative_item: str,
    assert_true: bool,
) -> None:
    """Test ``get_files``.

    Test for standard files, nested directories (only return the
    directory root) or files that are excluded.

    :param make_relative_file: Relative path to Python file.
    :param assert_relative_item: Relative path to Python item to check
        for.
    :param assert_true: Assert True or assert False.
    """
    project_dir = Path.cwd()
    make_file = project_dir / make_relative_file
    make_item = project_dir / assert_relative_item
    make_file.parent.mkdir(exist_ok=True, parents=True)
    make_file.touch()
    git.add(".")
    lsfiles.add_exclusions(WHITELIST_PY)
    lsfiles.populate()
    if assert_true:
        assert make_item in lsfiles.reduce()
    else:
        assert make_item not in lsfiles.reduce()


def test_files_exclude_venv(lsfiles, make_tree: t.Any) -> None:
    """Test that virtualenv dir is excluded.

     Test when indexing with ``PythonItems.items``.

    :param make_tree: Create directory tree from dict mapping.
    """
    project_dir = Path.cwd()
    make_tree(
        project_dir,
        {
            REPO: {"src": {INIT: None}},
            "venv": {
                "pyvenv.cfg": None,
                "bin": {},
                "include": {},
                "share": {},
                "src": {},
                "lib": {"python3.8": {"site-packages": {"six.py": None}}},
                "lib64": "lib",
            },
        },
    )

    # add venv to .gitignore
    with open(project_dir / GITIGNORE, "w", encoding="utf-8") as fout:
        fout.write("venv\n")

    lsfiles.clear()
    lsfiles.populate()
    assert set(lsfiles.reduce()) == set()


def test_seq(lsfiles) -> None:
    """Get coverage on ``Seq`` abstract methods."""
    lsfiles.append("key")
    assert lsfiles[0] == "key"
    lsfiles[0] = "value"
    assert lsfiles[0] == "value"
    del lsfiles[0]
    assert not lsfiles
    assert repr(lsfiles) == "<LSFiles []>"


def test_args_reduce(git, lsfiles, make_tree: t.Any) -> None:
    """Demonstrate why the ``reduce`` argument should be deprecated.

    No longer considered depreciated.

    :param make_tree: Create directory tree from dict mapping.
    """
    # ignore the bundle dir, including containing python files
    with open(Path.cwd() / GITIGNORE, "w", encoding="utf-8") as fout:
        fout.write("bundle")

    make_tree(
        Path.cwd(),
        {
            "dotfiles": {
                "vim": {
                    "bundle": {  # this dir should be ignored
                        "ctags": {
                            "Units": {
                                "parse-python.r": {
                                    "python-dot-in-import.d": {
                                        "input.py": None
                                    }
                                }
                            }
                        }
                    }
                },
                "ipython_config.py": None,
            },
            "src": {"__init__.py": None},
        },
    )
    git.add(".")
    lsfiles.populate()
    normal = lsfiles.args()
    reduced = lsfiles.args(reduce=True)

    # if reduce is used, then all of $PROJECT_DIR/dotfiles will be
    # scanned (as $PROJECT_DIR/dotfiles/ipython_config.py is not
    # ignored) therefore the .gitignore rule will not apply to
    # ``bundle``
    assert all(
        i in reduced
        for i in (str(Path.cwd() / "dotfiles"), str(Path.cwd() / "src"))
    )

    # therefore, the ``reduce`` argument should be used sparingly as in
    # this example the bundle dir will not be scanned
    assert all(
        i in normal
        for i in (
            str(Path.cwd() / "src" / "__init__.py"),
            str(Path.cwd() / "dotfiles" / "ipython_config.py"),
        )
    )


def test_files_extend_no_dupes(lsfiles) -> None:
    """Test files extend does not index duplicates."""
    files_before = sorted(
        [
            Path.cwd() / "dir" / "file1.py",
            Path.cwd() / "dir" / "file1.py",
            Path.cwd() / "file2.py",
        ]
    )
    files_after = sorted(
        [Path.cwd() / Path("dir", "file1.py"), Path.cwd() / Path("file2.py")]
    )
    lsfiles.extend(files_before)
    assert sorted(lsfiles) == files_after
