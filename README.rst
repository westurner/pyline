===============================
pyline
===============================


`GitHub`_ |
`PyPi`_ |
`Warehouse`_ |
`ReadTheDocs`_ |
`Travis-CI`_


.. image:: https://badge.fury.io/py/pyline.png
   :target: http://badge.fury.io/py/pyline
    
.. image:: https://travis-ci.org/westurner/pyline.png?branch=master
        :target: https://travis-ci.org/westurner/pyline

.. image:: https://pypip.in/d/pyline/badge.png
       :target: https://pypi.python.org/pypi/pyline

.. _GitHub: https://github.com/westurner/pyline
.. _PyPi: https://pypi.python.org/pypi/pyline
.. _Warehouse: https://warehouse.python.org/project/pyline
.. _ReadTheDocs:  https://pyline.readthedocs.org/en/latest
.. _Travis-CI:  https://travis-ci.org/westurner/pyline

Pyline is a grep-like, sed-like, awk-like command-line tool for
line-based text processing in Python.

.. contents:: 

Features
==========

* Compatibility with the `original pyline recipe`_
* Python `str.split`_ by an optional delimiter str (``-F``, ``--input-delim``)
* `Python regex`_ (``-r``, ``--regex``, ``-R``, ``--regex-options``)
* Output as `txt`, `csv`, `tsv`, `json`, `html` (``-O csv``, ``--output-filetype=csv``)
* Output as Markdown/ReStructuredText checkboxes (``-O checkbox``, ``--output-filetype=checkbox``)
* Lazy sorting (``-s``, ``--sort-asc``; ``-S``, ``--sort-desc``)
* Create `path.py <https://pypi.python.org/pypi/path.py>`__
  (or `pathlib`_) objects from each line (``-p``,
  ``--path-tools``)
* Functional `namedtuples`_, `iterators`_ ``yield`` -ing `generators`_
* `optparse`_ argument parsing (``-h``, ``--help``)
* `cookiecutter-pypackage`_ project templating  


.. _path.py: https://pypi.python.org/pypi/path.py
.. _str.split: https://docs.python.org/2/library/stdtypes.html#str.split
.. _Python regex: https://docs.python.org/2/library/re.html   
.. _pathlib: https://pypi.python.org/pypi/pathlib
.. _namedtuples: https://docs.python.org/2/library/collections.html#collections.namedtuple 
.. _iterators: https://docs.python.org/2/howto/functional.html#iterators
.. _generators: https://docs.python.org/2/howto/functional.html#generators    
.. _optparse: https://docs.python.org/2/library/optparse.html 
.. _cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage 


Why
=====
Somewhat unsurprisingly, I found the `original pyline recipe`_
while searching for "python grep sed"
(see ``AUTHORS.rst`` and ``LICENSE.psf``).

I added an option for setting ``p = Path(line)``
in the `eval`_/`compile`_ command context and `added it to my dotfiles
<https://github.com/westurner/dotfiles/commits/master/src/dotfiles/pyline.py>`_
; where it grew tests and an ``optparse.OptionParser``; and is now
promoted to a `GitHub`_ project with `ReadTheDocs`_ documentation,
tests with tox and `Travis-CI`_, and a setup.py for `PyPi`_.


.. _original Pyline recipe: https://code.activestate.com/recipes/437932-pyline-a-grep-like-sed-like-command-line-tool/
.. _eval: https://docs.python.org/2/library/functions.html#eval
.. _compile: https://docs.python.org/2/library/functions.html#compile
.. _MapReduce: https://en.wikipedia.org/wiki/MapReduce


What
======
Pyline is an ordered `MapReduce`_ tool:

Input Readers:
    * stdin (default)
    * file (``codecs.open(file, 'r', encoding='utf-8')``)

Map Functions:
    * Python module imports (``-m os``)
    * Python regex pattern (``-r '\(.*\)'``)
    * path library (``p`` from ``--pathpy`` OR ``--pathlib``)
    * Python codeobj **eval** output transform:

      .. code:: bash

         ls | pyline -m os 'line and os.path.abspath(line.strip())'
         ls | pyline -r '\(.*\)' 'rgx and (rgx.group(0), rgx.group(1)) or line'
         ls | pyline -p 'p and p.abspath() or ("# ".format(line))'

         # With an extra outer loop to bind variables in
         # (because (_p = p.abspath(); <codeobj>) does not work)
         find $PWD | pyline --pathpy -m os -m collections --input-delim='/' \
             'p and [collections.OrderedDict((
                     ("p", p),
                     ("_p", _p),
                     ("_p.split()", str(_p).split(os.path.sep)),
                     ("line.rstrip().split()", line.rstrip().split(os.path.sep)),
                     ("l.split()", l.split(os.path.sep)),
                     ("words", words),
                     ("w", w)))
                 for _p in [p.abspath()]][0]' \
                -O json

Partition Function:
    None

Compare Function:
    ``Result(collections.namedtuple).__cmp__``

Reduce Functions:
    ``bool()``,  ``sorted()``

Output Writers:
    ``ResultWriter`` classes

    .. code:: bash

       pyline -O csv
       pyline -O tsv
       pyline -O json


Installing
============
Install from `PyPi`_::

    pip install pyline

Install from `GitHub`_ as editable (add a ``pyline.pth`` in ``site-packages``)::

    pip install -e git+https://github.com/westurner/pyline#egg=pyline


Usage
=========

Print help::

    pyline --help

Process::

    # Print every line (null transform)
    cat ~/.bashrc | pyline line
    cat ~/.bashrc | pyline l

    # Number every line
    cat ~/.bashrc | pyline -n l

    # Print every word (str.split(input-delim=None))
    cat ~/.bashrc | pyline words
    cat ~/.bashrc | pyline w

    # Split into words and print (default: tab separated)
    cat ~/.bashrc | pyline 'len(w) >= 2 and w[1] or "?"'

    # Select the last word, dropping lines with no words
    pyline -f ~/.bashrc 'w[-1:]'

    # Regex matching with groups
    cat ~/.bashrc | pyline -n -r '^#(.*)' 'rgx and rgx.group()'
    cat ~/.bashrc | pyline -n -r '^#(.*)'

    ## Original Examples
    # Print out the first 20 characters of every line
    tail access_log | pyline "line[:20]"

    # Print just the URLs in the access log (seventh "word" in the line)
    tail access_log | pyline "words[6]"

Work with paths and files::

    # List current directory files larger than 1 Kb
    ls | pyline -m os \
      "os.path.isfile(line) and os.stat(line).st_size > 1024 and line"

    # List current directory files larger than 1 Kb
    #pip install path.py
    ls | pyline -p 'p and p.size > 1024 and line'


Documentation
==============
https://pyline.readthedocs.org/en/latest/


License
========
`Python Software License
<https://github.com/westurner/pyline/blob/master/LICENSE.psf>`_
