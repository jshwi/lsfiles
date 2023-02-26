"""
tests._test
===========
"""
from pathlib import Path

import pytest
from gitspy import Git

from lsfiles import LSFiles

from . import DIR, DOTFILES, FILE_1, NESTED, SRC, WHITELIST, FixtureMakeTree
from ._environ import FILES, GITIGNORE, INIT, REPO, WHITELIST_PY


@pytest.mark.parametrize(
    "make_relative_file,assert_relative_item,assert_true",
    [
        (FILES, FILES, True),
        (Path(NESTED) / "python" / "file" / FILES, NESTED, True),
        (WHITELIST_PY, WHITELIST, False),
    ],
    ids=["file", NESTED, "exclude"],
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

    :param git: Instantiated ``Git`` object.
    :param lsfiles: Instantiated ``LSFiles`` object.
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
    lsfiles.populate(str(WHITELIST))
    if assert_true:
        assert make_item in lsfiles.reduce()
    else:
        assert make_item not in lsfiles.reduce()


def test_files_exclude_venv(
    lsfiles: LSFiles, make_tree: FixtureMakeTree
) -> None:
    """Test that virtualenv dir is excluded.

     Test when indexing with ``PythonItems.items``.

    :param lsfiles: Instantiated ``LSFiles`` object.
    :param make_tree: Create directory tree from dict mapping.
    """
    project_dir = Path.cwd()
    make_tree(
        project_dir,
        {
            REPO: {SRC: {INIT: None}},
            "venv": {
                "pyvenv.cfg": None,
                "bin": {},
                "include": {},
                "share": {},
                SRC: {},
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


def test_seq(lsfiles: LSFiles) -> None:
    """Get coverage on ``Seq`` abstract methods.

    :param lsfiles: Instantiated ``LSFiles`` object.
    """
    lsfiles.append("key")  # type: ignore
    assert lsfiles[0] == "key"
    lsfiles[0] = "value"  # type: ignore
    assert lsfiles[0] == "value"
    del lsfiles[0]
    assert not lsfiles
    assert repr(lsfiles) == "<LSFiles []>"


def test_args_reduce(
    git: Git, lsfiles: LSFiles, make_tree: FixtureMakeTree
) -> None:
    """Demonstrate why the ``reduce`` argument should be deprecated.

    No longer considered depreciated.

    :param git: Instantiated ``Git`` object.
    :param lsfiles: Instantiated ``LSFiles`` object.
    :param make_tree: Create directory tree from dict mapping.
    """
    # ignore the bundle dir, including containing python files
    with open(Path.cwd() / GITIGNORE, "w", encoding="utf-8") as fout:
        fout.write("bundle")

    make_tree(
        Path.cwd(),
        {
            DOTFILES: {
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
            SRC: {"__init__.py": None},
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
        for i in (str(Path.cwd() / DOTFILES), str(Path.cwd() / SRC))
    )

    # therefore, the ``reduce`` argument should be used sparingly as in
    # this example the bundle dir will not be scanned
    assert all(
        i in normal
        for i in (
            str(Path.cwd() / SRC / "__init__.py"),
            str(Path.cwd() / DOTFILES / "ipython_config.py"),
        )
    )


def test_files_extend_no_dupes(lsfiles: LSFiles) -> None:
    """Test files extend does not index duplicates.

    :param lsfiles: Instantiated ``LSFiles`` object.
    """
    files_before = sorted(
        [
            Path.cwd() / DIR / FILE_1,
            Path.cwd() / DIR / FILE_1,
            Path.cwd() / "file2.py",
        ]
    )
    files_after = sorted(
        [Path.cwd() / Path(DIR, FILE_1), Path.cwd() / Path("file2.py")]
    )
    lsfiles.extend(files_before)
    assert sorted(lsfiles) == files_after


def test_regex(lsfiles: LSFiles, git: Git, make_tree: FixtureMakeTree) -> None:
    """Test populate with regex.

    :param lsfiles: Instantiated ``LSFiles`` object.
    :param git: Instantiated ``Git`` object.
    :param make_tree: Create directory tree from dict mapping.
    """
    path1 = Path.cwd() / "docs" / "conf.py"
    path2 = Path.cwd() / WHITELIST
    make_tree(Path.cwd(), {"docs": {"conf.py": None}, WHITELIST: None})
    git.add(".")
    lsfiles.populate_regex()
    assert path1 in lsfiles
    assert path2 in lsfiles
    lsfiles.clear()
    lsfiles.populate_regex(r"whitelist\.py|docs\/conf\.py")
    assert path1 not in lsfiles
    assert path2 not in lsfiles
