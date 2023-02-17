lsfiles
=======
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/lsfiles
    :target: https://pypi.org/project/lsfiles/
    :alt: PyPI
.. image:: https://github.com/jshwi/lsfiles/actions/workflows/build.yaml/badge.svg
    :target: https://github.com/jshwi/lsfiles/actions/workflows/build.yaml
    :alt: Build
.. image:: https://github.com/jshwi/lsfiles/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/lsfiles/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://results.pre-commit.ci/badge/github/jshwi/lsfiles/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/lsfiles/master
   :alt: pre-commit.ci status
.. image:: https://codecov.io/gh/jshwi/lsfiles/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/lsfiles
    :alt: codecov.io
.. image:: https://readthedocs.org/projects/lsfiles/badge/?version=latest
    :target: https://lsfiles.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
    :alt: isort
.. image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
    :target: https://github.com/PyCQA/docformatter
    :alt: docformatter
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint
    :alt: pylint
.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status
.. image:: https://snyk.io/test/github/jshwi/pyaud/badge.svg
    :target: https://snyk.io/test/github/jshwi/pyaud/badge.svg
    :alt: Known Vulnerabilities
.. image:: https://snyk.io/advisor/python/lsfiles/badge.svg
    :target: https://snyk.io/advisor/python/lsfiles
    :alt: lsfiles

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
    >>> files = LSFiles()
    >>> files.populate(f".*\/{p1.name}")
    >>>
    >>> ps = [str(p) for p in files]
    >>>
    >>> assert not str(p1) in ps
    >>> assert str(p2) in ps
