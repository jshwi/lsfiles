lsfiles
=======
.. image:: https://github.com/jshwi/lsfiles/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/lsfiles/actions/workflows/ci.yml
    :alt: ci
.. image:: https://github.com/jshwi/lsfiles/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/lsfiles/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://readthedocs.org/projects/lsfiles/badge/?version=latest
    :target: https://lsfiles.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/pypi/v/lsfiles
    :target: https://img.shields.io/pypi/v/lsfiles
    :alt: pypi
.. image:: https://codecov.io/gh/jshwi/lsfiles/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/lsfiles
    :alt: codecov.io
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/
    :alt: mit
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

Path object VC index
--------------------

Index versioned .py files

Install
-------

``pip install lsfiles``

Development
-----------

``poetry install``

Usage
-----


The ``LSFiles`` instance is a list-like object instantiated with an empty index

.. code-block:: python

    >>> from lsfiles import LSFiles
    >>> from pathlib import Path
    >>>
    >>> files = LSFiles()
    >>> files
    <LSFiles []>


The ``LSFiles`` index calls ``git ls-files`` and only versioned files are indexed

.. code-block:: python

    >>> files.populate()
    >>> for path in sorted([p.relative_to(Path.cwd()) for p in files]):
    ...     print(path)
    docs/conf.py
    lsfiles/__init__.py
    lsfiles/_indexing.py
    lsfiles/_objects.py
    lsfiles/_version.py
    tests/__init__.py
    tests/_environ.py
    tests/_test.py
    tests/conftest.py
    whitelist.py

The ``LSFiles`` instance is an index of unique file paths

It's implementation of ``extend`` prevents duplicates

.. code-block:: python

    >>> p1 = Path.cwd() / "f1"
    >>> p2 = Path.cwd() / "f1"
    >>>
    >>> files = LSFiles()
    >>> files.extend([p1, p2])
    >>> sorted([p.relative_to(Path.cwd()) for p in files.reduce()])
    [PosixPath('f1')]

Reduce minimizes index to directories and individual files relative to the current working dir

The list value is returned, leaving the instance unaltered

.. code-block:: python

    >>> p1 = Path.cwd() / "f1"
    >>>
    >>> d = Path.cwd() / "dir"
    >>> p2 = d / "f2"
    >>> p3 = d / "f3"
    >>>
    >>> files = LSFiles()
    >>> files.extend([p1, p2, p3])
    >>> sorted(p.relative_to(Path.cwd()) for p in files.reduce())
    [PosixPath('dir'), PosixPath('f1')]

Exclusions can be added on instantiation

Exclusions are evaluated by their basename, and does not have to be an absolute path

.. code-block:: python

    >>> p1 = Path.cwd() / "docs" / "conf.py"
    >>> p2 = Path.cwd() / "lsfiles" / "__init__.py"
    >>>
    >>> files = LSFiles(p1.name)
    >>> files.populate()
    >>>
    >>> ps = [str(p) for p in files]
    >>>
    >>> assert not str(p1) in ps
    >>> assert str(p2) in ps
