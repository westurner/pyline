.. :changelog:

History
=========

release/0.3.20 (2020-10-02 20:51:19 -0400)
++++++++++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.19..release/0.3.20

* MRG: Merge tag 'v0.3.19' into develop \[fc2163e\]
* BLD: setup.py: 3 & 3.8 trove classifiers \[6bf10e0\]
* RLS: pyline.py,setup.py: v0.3.20 \[242a75a\]


v0.3.19 (2020-10-02 20:44:25 -0400)
+++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.18..v0.3.19

* MRG: Merge tag 'v0.3.18' into develop \[715618e\]
* DOC,BLD: HISTORY.rst: \*manually\* fix unquoted/unescaped reference \[9146f39\]
* BLD: setup.cfg: \[wheel\] -> \[bdist_wheel\] \[ba27bd5\]
* BLD: setup.py: long_description_content_type='text/x-rst' \[07dc247\]
* RLS: pyline.py,setup.py: v0.3.19 \[405f3f6\]
* DOC: HISTORY.rst: output from git-changelog.py \[9088f29\]
* MRG: Merge branch 'release/0.3.19' \[45110ec\]


v0.3.18 (2020-10-02 20:27:08 -0400)
+++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.17..v0.3.18

* MRG: Merge tag 'v0.3.17' into develop \[09f46ca\]
* REF,TST: Makefile, requirements-test: switch to pytest, require jinja2 for tests \[999446d\]
* REF,TST: pyline.py, test_pyline.py: py3 \[7365938\]
* WIP: __init__: change import for py3 (TODO: check py2 compatibility) \[fe61a93\]
* BLD: requirements\[-test\]: remove wheel, -test -> reqs.txt \[716a9b3\]
* REF,BUG: py3, pathpy import, rawstrs, only strip one newline when numbering lines \[f7b3281\]
* BLD: tox.ini,.travis.yml: use tox-travis, envs=py37,py38 \[a2a4a82\]
* DOC,BLD: docs/reqs,docs/conf: copyright, fix pyline import \[036bac8\]
* BLD,TST: setup.py: setup.py:test calls pytest -v \[ced27bb\]
* REF,BUG: pyline.py: when sorting, sort None as '' (and log extensively for other sort comparison TypeError exceptions) \[9248acb\]
* MRG: #29 REF,TST,BLD,BUG: Python 3 Support \[cb195b4\]
* REF: pyline.py: change shebang to \`#!/usr/bin/env python\` from python2 \[5841704\]
* RLS: pyline.py,setup.py: v0.3.18 \[a1072e2\]
* DOC: HISTORY.rst: output from git-changelog.py \[c9f7f89\]
* MRG: Merge branch 'release/0.3.18' \[579ccdf\]



v0.3.17 (2018-12-23 14:41:45 -0500)
+++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.16..v0.3.17

* MRG: Merge tag 'v0.3.15' into develop \[e1d7768\]
* MRG: Merge tag 'v0.3.16' into develop \[3a6fec4\]
* DOC: pyline.py: typo: checkbok -> checkbox \[a0917c5\]
* BUG,ENH: pyline.py: -p: strip one trailing '\n' from line before parsing as path \[47efdc9\]
* RLS: setup.py, pyline.py: v0.3.17 \[9ef9d41\]
* BLD,DOC: Makefile: setversion, release docs \[5cfc1e4\]
* MRG: Merge branch 'release/0.3.17' \[618920a\]


v0.3.16 (2016-07-22 11:42:57 -0500)
+++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.15..v0.3.16

* BUG: pyline.py: sys.argv\[1:\] (#7) \[a548405\]
* RLS: pyline v0.3.16 \[b17153a\]
* DOC: HISTORY.rst: git-changelog.py \[9725f8d\]
* MRG: Merge branch 'hotfix/0.3.16' \[c18d61c\]


v0.3.15 (2016-07-22 11:34:56 -0500)
+++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.14..v0.3.15

* MRG: Merge tag 'v0.3.12' into develop \[b4a3ec7\]
* BUG: include files named \s+ with -p/--pathpy or --pathlib (fixes #24) \[6c3f658\]
* MRG: Merge tag 'v0.3.13' into develop \[1f2b64b\]
* MRG: Merge tag 'v0.3.14' into develop \[b27731a\]
* ETC: pyline/__init__.py: __version__ = version = pyline.version \[4065820\]
* RLS: setup.py, pyline.py: version='0.3.15' \[a83ad49\]
* DOC: HISTORY.rst: git-changelog.py -r "release/0.3.15" --hdr="+"\` \[cfd26be\]
* MRG: Merge branch 'release/0.3.15' \[2225fd6\]


v0.3.14 (2016-07-22 11:27:03 -0500)
+++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.13..v0.3.14

* BUG: pyline/__init__.py: remove untested package-level __main__ function \[91e1f5f\]
* RLS: setup.py, __init__.py, pyline.py: v0.3.14 (in 3 places) \[3186eb5\]
* MRG: Merge branch 'hotfix/0.3.14' \[527df85\]


v0.3.13 (2016-07-22 11:16:44 -0500)
+++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.12..v0.3.13

* BUG,TST: pyline/pyline.py: console_entrypoint -> pyline.pyline:main_entrypoint (see: #7) \[a16570e\]
* MRG: Merge branch 'hotfix/0.3.13' \[29b64ef\]


v0.3.12 (2016-02-16 16:07:18 -0600)
+++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.11..v0.3.12

* MRG: Merge tag 'v0.3.11' into develop \[98adc78\]
* DOC: README.rst: add \.. contents:: \[4416581\]
* TST,UBY: pyline.py, scripts/pyline.py: symlinks to pyline/pyline.py \[2fda52e\]
* UBY,BUG: pyline.py: loglevels \[WARN\], -v/--verbose/DEBUG, -q/--quiet/ERROR \[07fbc09\]
* RLS,DOC: setup.py,pyline.py: version 0.3.12 \[0cb05f3\]
* DOC: HISTORY.rst: git-changelog.py --hdr=+ --rev 'release/0.3.12' \| pbcopy \[3b4d775\]
* MRG: Merge branch 'release/0.3.12' \[29332e2\]


v0.3.11 (2016-02-14 22:29:55 -0600)
+++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.10..v0.3.11

* MRG: Merge tag 'v0.3.10' into develop \[ed296ea\]
* BLD: tox.ini: testenv/deps/jinja2 \[1a6c2f5\]
* BLD: tox.ini, requirements.txt: add jinja2 to requirements.txt \[e267a1e\]
* RLS,DOC: setup.py,pyline.py: version 0.3.11 \[21bd6e9\]
* DOC: HISTORY.rst: git-changelog.py --hdr=+ --rev 'release/0.3.11' \| pbcopy \[efc24ce\]
* MRG: Merge branch 'release/0.3.11' \[9c05df0\]


v0.3.10 (2016-02-14 21:56:36 -0600)
+++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.9..v0.3.10

* MRG: Merge tag 'v0.3.9' into develop \[f7c8a16\]
* BUG,UBY: pyline.py: logging config (default INFO, -q/--quiet, -v/--verbose (DEBUG)) \[8a060ab\]
* UBY,DOC: pyline.py: log.info(('pyline.version', __version__)) at startup \[da1e883\]
* BUG,UBY: pyline.py: log.info(('argv', argv)) \[ede1d5e\]
* BUG,REF: opts\['cmd'\], main->(int, results\[\]), log opts after all config \[3cf9585\]
* UBY: pyline.py: log.info(('_rgx', _regexstr)) \[02bd234\]
* RLS,DOC: setup.py,pyline.py: version 0.3.10 \[ea6a1fd\]
* DOC: HISTORY.rst: git-changelog.py --hdr=+ --rev 'release/0.3.10' \| pbcopy \[5266662\]
* MRG: Merge branch 'release/0.3.10' \[aa2529a\]


v0.3.9 (2016-02-14 17:58:36 -0600)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.8..v0.3.9

* ENH: pyline.py: --version arg \[a38bf5a\]
* MRG: Merge tag 'v0.3.8' into develop \[85cd8e9\]
* BUG,REF: pyline.py: output-filetype/-> output-format \[fbcd9e2\]
* BUG: pyline.py: only print version when opts.get('version') \[ef8ac20\]
* RLS,DOC: setup.py,pyline.py: version 0.3.9 \[5f2c4a6\]
* DOC: HISTORY.rst: git-changelog.py --hdr=+ --rev 'release/0.3.9' \| pbcopy \[ce95bae\]
* MRG: Merge branch 'release/0.3.9' \[38e0393\]


v0.3.8 (2016-02-14 17:34:08 -0600)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.7..v0.3.8

* MRG: Merge tag 'v0.3.7' into develop \[0cd0e3c\]
* BUG,ENH: fix CSV header row; add -O jinja:template=path.jinja support (#1,) \[d5fe67b\]
* ENH: pyline.py: --version arg \[818fc1d\]
* RLS: setup.py, pyline.py: version 0.3.8 \[245214d\]
* DOC: HISTORY.rst: git-changelog.py --hdr=+ --rev 'release/0.3.8' \| pbcopy \[983b535\]
* DOC: HISTORY.rst: git-changelog.py --hdr=+ --rev 'release/0.3.8' \| pbcopy \[7b65d8e\]
* MRG: Merge branch 'release/0.3.8' \[2f5f249\]


v0.3.7 (2016-02-12 20:04:39 -0600)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.6..v0.3.7

* Merge tag 'v0.3.5' into develop \[8c5de0a\]
* ENH: pyline.py: main(args=None, iterable=None, output=None) \[dd490e1\]
* UBY: pyline.py: -O chk == -O checkbox \[3aa96ce\]
* UBY: pyline.py: l = line = o = obj \[3aa9a81\]
* DOC: pyline.py: -f/--in/--input-file, -o/--out/--output-file \[bcc9eff\]
* TST: requirements-test.txt: nose, nose-parameterized, nose-progressive \[213e0c0\]
* BUG: pyline: collections.OrderedDict, return 0 \[5fd1114\]
* DOC: setup.py: install_requires=\[\] \[a41bf30\]
* TST,BUG,CLN: test_pyline.py: chk, main(_args), docstrings, #opts._output.close() \[0254f30\]
* Merge tag 'v0.3.6' into develop \[f46f90c\]
* DOC,REF: pyline.py: type_func->typefunc, docstrings \[08c8d9c\]
* UBY: pyline.py: \[--input-delim-split-max\|--max\|--max-split\] \[b509726\]
* REF: pyline.py: ResultWriter.get_writer ValueError, expand \[143c5f7\]
* DOC: pyline.py: usage docstring, main docstring \[bc44747\]
* TST: tests/test_pylinepy: more tests of sorting \[b60750a\]
* DOC: pyline.py: docstrings \[89ea5c7\]
* BLD,TST,BUG: Makefile, setup.py, pyline.py, test_pyline.py: pyline.main does sorting, kwargs, opts obj \[e80cde6\]
* TST,REF: split to SequenceTestCase, LoggingTestCase, Test\* \[62ff39b\]
* TST: tests/test_pyline.py: TestPylinePyline.test_30_pyline_codefunc \[49928d5\]
* Merge branch 'feature/split_tests' into develop \[ef63a18\]
* RLS,DOC: README.rst, setup.py, pyline.py 0.3.7 description \[9fc262e\]
* Merge branch 'release/0.3.7' \[07b00b2\]


v0.3.6 (2015-12-21 04:17:23 -0600)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.5..v0.3.6

* BUG: pyline.py: #!/usr/bin/env python2 \[9729816\]
* RLS: HISTORY.rst, __init__.py, pyline.py, setup.py: __version__ = '0.3.6' \[a463d39\]
* Merge branch 'hotfix/0.3.6' \[445c089\]


v0.3.5 (2015-05-24 20:58:39 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.4..v0.3.5

* Merge tag 'v0.3.4' into develop \[3ec1391\]
* CLN: patchheader: rm \[c9f6304\]
* ENH: pyline.py: add a codefunc() kwarg \[be8dcc8\]
* BUG,DOC: pyline.py: set default regex_options to '', optparse helpstrings \[fa9e9cb\]
* DOC: pyline.py: docstrings (calling a function, stdlib/vendoring) \[ee22e2c\]
* ENH,TST: pyline.py: add a codefunc() kwarg \[91aa0a8\]
* RLS: setup.py, __init__, HISTORY: v0.3.5, git log --format='\* %s \[%h\]' master..develop \[78f3ad9\]
* Merge branch 'release/0.3.5' \[065797d\]


v0.3.4 (2015-04-25 06:48:47 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.3..v0.3.4

* Merge tag 'v0.3.3' into develop \[e630114\]
* RLS: HISTORY.rst, __init__.py, setup.py: v0.3.4 \[e448183\]
* Merge branch 'release/0.3.4' \[612228d\]


v0.3.3 (2015-04-25 06:43:37 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.2..v0.3.3

* Merge tag 'v0.3.2' into develop \[061840b\]
* BUG: pyline.pyline.__main__ \[db71796\]
* DOC,BLD,CLN: Makefile: sphinx-apidoc --no-toc \[209bff8\]
* TST,CLN: pyline.py: remote -t/--test option \[2629924\]
* DOC,CLN: modules.rst: remove generated modules.rst \[abdc00d\]
* BUG, ENH, BUG, TST: \[b5a21e7\]
* RLS: __init__.py, setup.py: v0.3.3 \[eb81129\]
* BLD: Makefile: release (dist), twine \[7e602c8\]
* Merge branch 'release/0.3.3' \[c0df4ab\]


v0.3.2 (2014-11-30 19:49:42 -0600)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.1..v0.3.2

* Merge tag 'v0.3.1' into develop \[a3f8c1c\]
* ENH: Add pyline.__main__ (pyline.pyline.main) for 'python -m pyline' \[1bd5e10\]
* DOC: README.rst \[a26d97a\]
* DOC: HISTORY.rst: link to Source: http://code.activestate.com/recipes/437932-pyline-a-grep-like-sed-like-command-line-tool/ \[5871727\]
* DOC: usage.rst: add :shell: option to 'pyline --help' output \[d1f32de\]
* BUG: pyline/__init__.py: Set pyline.pyline.__main__ correctly \[49ae891\]
* DOC: pyline/pyline.py: docstrings, import path as pathpy \[178af4e\]
* RLS: HISTORY.txt, pyline/__init__.py, setup.py: set version to v0.3.2 \[6c547e4\]
* Merge branch 'release/0.3.2' \[10b84f5\]


v0.3.1 (2014-10-27 07:53:27 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.3.0..v0.3.1

* Merge tag 'v0.3.0' into develop \[35a380b\]
* DOC: README.rst \[f803665\]
* Merge branch 'hotfix/readme-travis-link' \[35f7b44\]
* Merge tag 'vreadme-travis-link' into develop \[6849887\]
* DOC: setup.py version 0.3.1 \[a7fae60\]
* Merge branch 'release/0.3.1' \[276d16b\]


v0.3.0 (2014-10-27 07:34:58 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.2.0..v0.3.0

* Added tag v0.2.0 for changeset cddc5c513cd2 \[c53a725\]
* DOC: Update README.rst: typo -output-filetype -> --output-filetype \[6897954\]
* DOC: Update README.rst: update 'Features' \[548c426\]
* DOC: Update README.rst: update 'Features' \[273b475\]
* DOC: Update README.rst: update 'Features' \[254ed95\]
* DOC: Update README.rst add additional link to docs \[8415a7c\]
* BLD,DOC: Update requirements.txt: add ../ (from ./docs) as editable \[d94ff0e\]
* Revert "BLD,DOC: Update requirements.txt: add ../ (from ./docs) as editable" \[fa062b8\]
* DOC: program-output:: -> command-output:: \[984b8a6\]
* ENH,BUG,CLN: #10, #12, #13 \[a75d2f9\]
* CLN: remove _import_path_module \[0cc9bb9\]
* RLS: pyline v0.3.0 \[14941af\]
* Merge branch 'release/0.3.0' \[53609dc\]


v0.2.0 (2014-08-24 14:44:31 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.1.5..v0.2.0

* Added tag v0.1.5 for changeset 8cd9c44a80ab \[4bb3fc7\]
* BLD: Add docs for 'make release'; remove bdist_wheel upload \[e76b592\]
* BLD: Add docs for 'make release': HISTORY.rst \[e5b3e9a\]
* ENH: Add checkbox output formatter (closes #5) \[46b7177\]
* BUG: add NullHandler to logger (closes #6) \[a9fac28\]
* RLS: Release v0.2.0 \[9ef4a25\]
* Added tag v0.2.0 for changeset f510a75a37a8 \[38c7eeb\]


v0.1.5 (2014-05-12 20:59:34 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.1.4..v0.1.5

* Added tag v0.1.4 for changeset c79a1068cb1c \[0abdc5e\]
* DOC: setup.py keywords and classifiers \[9079d03\]
* DOC: Update HISTORY.rst: 0.1.0 -> 0.1.5 \[9bfe2a5\]
* BLD: bump version to v0.1.5 \[0af9381\]


v0.1.4 (2014-05-12 20:42:52 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.1.3..v0.1.4

* Added tag v0.1.3 for changeset d49705961509 \[4f8cfec\]
* DOC: correct license and download_url in setup.py \[49ea953\]


v0.1.3 (2014-05-12 20:30:47 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.1.2..v0.1.3

* Added tag v0.1.2 for changeset 09cca8fa5555 \[828d223\]
* DOC: missing newline in description \[63a442c\]
* DOC: version bump, setup description \[53ad0f4\]


v0.1.2 (2014-05-12 20:24:26 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.1.1..v0.1.2

* Added tag v0.1.1 for changeset 13ad121ea966 \[5727951\]
* BLD: add pathlib and path.py to requirements.txt \[aa6dda7\]
* DOC,BLD,BUG: setup.py build_long_description, file handles \[f7a73c1\]
* DOC: README.rst: remove includes \[2d2bd6f\]
* DOC: version bump, setup description \[e920ff2\]


v0.1.1 (2014-05-12 19:41:54 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' v0.1.0..v0.1.1

* DOC,BLD: Update AUTHORS.rst, HISTORY.rst, README.rst, docs/license.rst \[7b087c8\]
* CLN: pyline rename arg\[0\] _input -> iterable \[7040271\]
* BUG: default command in -- ls \| pyline -p  " p = path = Path(line.strip()) \[30dce3a\]
* LOG: log.info(cmd) .\.. after shell parsing, exception \[c449765\]
* CLN: pep8 test command kwargs formatting \[993c65a\]
* DOC: README.rst; ReST doesn't seem to like \`path.py\`_ \.. _path.py:, links \[209ecb5\]
* TST: Update setup.py test command (runtests -v ./tests/test\*.py) \[bc84652\]
* TST: tox.ini: make html rather than sphinx-build \[c96b3b0\]
* CLN: factor out _import_pathmodule and get_path_module \[d0aebfb\]
* TST: move tests from pyline.py to tests/test_pyline.py \[477fbb4\]
* BUG: file handles (was causing tests to fail silently) \[80e84b6\]
* CLN: move optparse things into get_option_parser() \[723a8b7\]
* BLD: Release 0.1.1 \[3f9f56f\]


v0.1.0 (2014-05-12 04:03:15 -0500)
++++++++++++++++++++++++++++++++++
::

   git log --reverse --pretty=format:'* %s [%h]' b1303ba..v0.1.0

* CLN: Update .gitignore and .hgignore \[0d07ad1\]
* DOC: Update README.rst: comment out unconfigured badges \[b0e0fc1\]
* ENH: Add pyline script from https://github.com/westurner/dotfiles/blob/e7f766f3/src/dotfiles/pyline.py \[ce2dba8\]
* BLD,TST: Add py.test runtests.py and setup.py:PyTestCommand \[953edbe\]
* BUG: try/except import StringIO (Python 3 compatibility) \[97d5781\]
* BLD: remove py33 section from tox.ini for now \[b103587\]
* BLD: remove py33 section from tox.ini for now \[2ff4a77\]
* BLD: Update tox.ini, .travis.yml, reqs, docs/conf \[13b5487\]
* CLN: pyline cleanup \[9724f8e\]
* CLN: update .hgignore \[59196b7\]




0.0.1 (Unreleased)
+++++++++++++++++++
| Source: http://code.activestate.com/recipes/437932-pyline-a-grep-like-sed-like-command-line-tool/

* Updated 2012.11.17, Wes Turner
* Updated 2005.07.21, thanks to Jacob Oscarson
* Updated 2006.03.30, thanks to Mark Eichin

