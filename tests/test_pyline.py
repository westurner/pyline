#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
test_pyline
----------------------------------

Tests for `pyline` module.
"""

import unittest

from pyline import pyline

TEST_INPUT = """
Lines
=======
Of a file
---------
With Text

And Without

http://localhost/path/to/file?query#fragment

"""
import logging
import tempfile
import os
import sys
try:
    import StringIO as io   # Python 2
except ImportError:
    import io               # Python 3


class TestPyline(unittest.TestCase):

    def setUp(self, *args):
        self.setup_logging()
        (self._test_file_fd, self.TEST_FILE) = tempfile.mkstemp(text=True)
        fd = self._test_file_fd
        os.write(fd, TEST_INPUT)
        os.write(fd, self.TEST_FILE)
        self.log.info("setup: %r", repr(self.TEST_FILE))

    def setup_logging(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

    def tearDown(self):
        os.close(self._test_file_fd)
        os.remove(self.TEST_FILE)

    def test_10_pyline_pyline(self):
        PYLINE_TESTS = (
            {"cmd": "line"},
            {"cmd": "words"},
            {"cmd": "sorted(words)"},
            {"cmd": "w[:3]"},
            {"regex": r"(.*)"},
            {"regex": r"(.*)", "cmd": "rgx and rgx.groups()"},
            {"regex": r"(.*)", "cmd": "rgx and rgx.groups() or '#'"},
        )
        _test_output = sys.stdout
        for test in PYLINE_TESTS:
            for line in pyline.pyline(io.StringIO(TEST_INPUT), **test):
                print(line, file=_test_output)

    def test_20_pyline_main(self):
        CMDLINE_TESTS = (
            tuple(),
            ("line",),
            ("l",),
            ("l", "-n"),
            ("l and l[:5]",),
            ("words",),
            ("w",),
            ("w", "-n"),
            ("w", '-O', 'csv'),
            ("w", '-O', 'csv', '-n'),

            ("w", '-O', 'csv', '-s', '0'),
            ("w", '-O', 'csv', '-s', '1'),
            ("w", '-O', 'csv', '-s', '1,2'),
            ("w", '-O', 'csv', '-S', '1'),
            ("w", '-O', 'csv', '-S', '1', '-n'),

            ("w", '-O', 'json'),
            ("w", '-O', 'json', '-n'),

            ("w", '-O', 'tsv'),

            ("w", '-O', 'html'),

            ("w", '-O', 'checkbox'),

            ("len(words) > 2 and words",),

            ('-r', '(.*with.*)'),
            ('-r', '(.*with.*)',            '-R', 'i'),
            ('-r', '(?P<line>.*with.*)'),
            ('-r', '(?P<line>.*with.*)',    '-O', 'json'),
            ('-r', '(?P<line>.*with.*)',    '-O', 'checkbox'),
            ('-r', '(.*with.*)', 'rgx and {"n":i, "match": rgx.groups()[0]}',
             '-O', 'json'),
            ("-r", '(.*with.*)', '_rgx.findall(line)',
             '-O', 'json'),

            ('-m',
             'os',
             'os.path.isfile(line) and (os.stat(line).st_size, line)'),
            #
            ("-p", "p and p.isfile() and (p.size, p, p.stat())")
        )

        TEST_ARGS = ('-f', self.TEST_FILE)

        for argset in CMDLINE_TESTS:
            _args = TEST_ARGS + argset
            self.log.debug("main%s" % str(_args))
            try:
                output = pyline.main(*_args)
                for n in output and output or []:
                    self.log.debug(n)
            except Exception as e:
                self.log.error("cmd: %s" % repr(_args))
                self.log.exception(e)
                raise


if __name__ == '__main__':
    unittest.main()
