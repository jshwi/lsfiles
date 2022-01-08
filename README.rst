lsfiles
=======
.. image:: https://github.com/jshwi/lsfiles/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/lsfiles/actions/workflows/ci.yml
    :alt: ci
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

Install
-------

``pip install lsfiles``

Development
-----------

``poetry install``

Usage
-----


.. code-block:: python

    >>> from lsfiles import LSFiles
    >>> from pathlib import Path
    >>> files = LSFiles()  # begin with an empty index
    >>> # the `LSFiles` object is a mutable sequence (list-like object)
    >>> print(files)
    <LSFiles []>
    >>> # `lsfiles` is designed to work with `git`, and only versioned files
    >>> # are indexed
    >>> # $ git init
    >>> files.populate()  # <LSFiles []>
    >>> # $ git add .
    >>> files.populate()  # <LSFiles [PosixPath(...), ...]>
    >>> files.clear()  # clear the index
    >>> print(files)
    <LSFiles []>
    >>> # as `lsfiles` is an index of unique file paths, its implementation
    >>> # of extend prevents duplicates
    >>> values = [Path.cwd() / "1", Path.cwd() / "1"]
    >>> files.extend(values)  # <LSFiles [PosixPath('.../lsfiles/1')]>
    >>> files.clear()
    >>> # reduce minimizes index to directories and individual files
    >>> # the list value is returned, leaving `LSFiles` unaltered
    >>> values = [
    ...     Path.cwd() / "f1",
    ...     Path.cwd() / 'd1' / "1",
    ...     Path.cwd() / 'd1' / "2",
    ... ]
    >>> files.extend(values)
    >>> files.reduce() # -> [PosixPath('.../f1'), PosixPath('.../d1')]
    >>> # exclusions are evaluated by their basename, and does not have
    >>> # have to be an absolute path
    >>> # exclusions can be added on instantiation
    >>> files = LSFiles("f1")
    >>> # or with the add exclusions method
    >>> files = LSFiles()
    >>> files.add_exclusions()
