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


TEST_INPUT_A0 = """a 5
b 4
c 3
d 2
e 1
f 0
"""

TEST_OUTPUT_A0_SORT_ASC_0 = TEST_INPUT_A0
TEST_OUTPUT_A0_SORT_DESC_0 = """f 0
e 1
d 2
c 3
b 4
a 5
"""
TEST_OUTPUT_A0_SORT_ASC_1 = TEST_OUTPUT_A0_SORT_DESC_0

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

    def test_15_pyline_sort(self):
        def split_to_words(s):
            return [x.split() for x in s.splitlines()]
        PYLINE_TESTS = (
            ({"cmd": "line", "sort_asc": "0"},
             TEST_OUTPUT_A0_SORT_ASC_0),
            ({"cmd": "words", "sort_asc": "0"},
             split_to_words(TEST_OUTPUT_A0_SORT_ASC_0)),

            ({"cmd": "words", "sort_asc": "1"},
             split_to_words(TEST_OUTPUT_A0_SORT_ASC_1)),

            # TODO: AssertRaises ? output w/ cmd "line" undef.

            # ({"cmd": "line", "sort_asc": "2"},
            # TEST_OUTPUT_A0_SORT_ASC_1),

            #({"cmd": "line", "sort_desc": "0"},
             #TEST_OUTPUT_A0_SORT_DESC_0),
            # ({"cmd": "words", "sort_desc": "0"},
            # split_to_words(TEST_OUTPUT_A0_SORT_DESC_0)),

            #{"cmd": "words"},
            #{"cmd": "w[:3]"},
            #{"regex": r"(.*)"},
            #{"regex": r"(.*)", "cmd": "rgx and rgx.groups()"},
            #{"regex": r"(.*)", "cmd": "rgx and rgx.groups() or '#'"},
        )
        _test_output = sys.stdout
        for kwargs, expected_output in PYLINE_TESTS:
            print(kwargs)
            output = list(pyline.pyline(io.StringIO(TEST_INPUT_A0), **kwargs))
            if isinstance(expected_output, basestring):
                expected_io = io.StringIO(expected_output)
            for result, expected_line in zip(output, expected_io):
                # strip trailing newline
                # _output_line = output_line.result[:-1]
                output_line = result.result
                print("out:", repr(output_line), file=_test_output)
                print("exp:", repr(expected_line), file=_test_output)
                print('-- output --')
                print(output)
                self.assertEqual(output_line, expected_line)

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
            ("w", "--shlex"),
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
