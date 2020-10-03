#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
test_pyline
----------------------------------

Tests for `pyline` module.
"""
import collections
import difflib
# import json
import logging
import os
import pprint
import sys
import tempfile
import types
import unittest

IS_PYTHON2 = sys.version_info.major == 2

try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest
    basestring = str

try:
    import StringIO as io   # Python 2
except ImportError:
    import io               # Python 3

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


TEST_INPUT_A0 = """a 5 320
b 4 310
c 3 200
d 2 100
e 1 500
f 0 300
"""

TEST_OUTPUT_A0_SORT_ASC_0 = TEST_INPUT_A0
TEST_OUTPUT_A0_SORT_DESC_0 = """f 0 300
e 1 500
d 2 100
c 3 200
b 4 310
a 5 320
"""
TEST_OUTPUT_A0_SORT_ASC_1 = TEST_OUTPUT_A0_SORT_DESC_0

TEST_OUTPUT_A0_SORT_ASC_2 = """d 2 100
c 3 200
f 0 300
b 4 310
a 5 320
e 1 500
"""

TEST_OUTPUT_A0_SORT_DESC_2 = '\n'.join(
    l for l in TEST_OUTPUT_A0_SORT_ASC_2.splitlines()[::-1]
)

_IO = collections.namedtuple('IO', ['args', 'kwargs', 'expectedoutput'])


def splitwords(s):
    return [x.split() for x in s.splitlines()]

class IO(_IO):

    def __repr__(self):
        # return json.dumps(self._asdict(), indent=2)
        return unicode(
            "IO(\n"
            "  args={}\n"
            "  kwargs={}\n"
            "  expected=\n"
            "{}\n"
            ")").format(
                repr(self.args),
                repr(self.kwargs),
                pprint.pformat(self.expectedoutput))


class SequenceTestCase(unittest.TestCase):
    @staticmethod
    def sequence_sidebyside(
            seq1,
            seq2,
            header1=None,
            header2=None,
            colwidth=None,
            colsplitstr=' | ',
            DEFAULT_COLWIDTH=36):
        """print seq1 and seq2  adjacently

        Args:
            seq1 (list[object.__repr__)): list of objects
            seq2 (list[object.__repr__]): list of objects
        Kwargs:
            header1 (None, str): header for col1
            header2 (None, str): header for col2
            colwidth (None):
        Returns:
            list: list of strings without newlines
                (of length ((2 * colwidth) + len(colsplitstr)))
        """
        header1 = header1 if header1 is not None else 'thing1'
        header2 = header2 if header2 is not None else 'thing2'
        obj1_repr_maxwidth = None
        # obj2_repr_maxwidth = None
        seq1_and_seq2 = []
        for obj1, obj2 in izip_longest(seq1, seq2):
            obj1_repr, obj2_repr = repr(obj1), repr(obj2)
            seq1_and_seq2.append((obj1_repr, obj2_repr,))
            obj1_repr_len = len(obj1_repr)
            if obj1_repr_len > obj1_repr_maxwidth:
                obj1_repr_maxwidth = obj1_repr_len
        if colwidth is None:
            if obj1_repr_maxwidth:
                colwidth = obj1_repr_maxwidth
            else:
                colwidth = DEFAULT_COLWIDTH

        def strfunc(str1, str2, colwidth=colwidth, colsplitstr=colsplitstr):
            return colsplitstr.join((
                str1.ljust(colwidth, ' '),
                str2.ljust(colwidth, ' ')))

        def draw_table():
            yield strfunc(header1, header2)
            yield strfunc('='*colwidth, '='*colwidth)
            for seqs in seq1_and_seq2:
                yield strfunc(*seqs)
            yield strfunc('_' * colwidth, '_' * colwidth)
        tblstr = list(draw_table())
        # for line in tblstr:
        #     print(line)
        return tblstr, colwidth

    @staticmethod
    def sequence_updown(seq1, seq2, maxwidth=None):
        yield str(seq1)[:maxwidth]
        yield str(seq2)[:maxwidth]

    def assertSequenceEqualSidebyside(self,
            seq1, seq2, seq_type=None, msg=None,
            header1=None, header2=None, colwidth=None):
        """print seq1 and seq2  adjacently

        Args:
            seq1 (list[object)): list of objects with ``__repr__`` methods
            seq2 (list[object]): list of objects with ``__repr__`` methods
        Kwargs:
            header1 (None, str): header for col1
            header2 (None, str): header for col2
            colwidth (None):
        Raises:
            list: list of strings without newlines
                (of length ((2 * colwidth) + len(colsplitstr)))
        """
        seq1_str = pprint.pformat(seq1) #.splitlines() # [repr(x) for x in seq1])
        seq2_str = pprint.pformat(seq2) #.splitlines() # [repr(x) for x in seq2))
        #import pdb; pdb.set_trace()  # XXX BREAKPOINT

        header1 = 'expected'
        header2 = 'output'
        try:
            self.assertSequenceEqual(
                seq1, seq2,
                seq_type=seq_type,
                msg=msg)
            self.assertMultiLineEqual(
                seq1_str,
                seq2_str,
                msg=msg)
        except AssertionError as e:
            sidebysidestr, colwidth = self.sequence_sidebyside(
                seq1, seq2,
                header1=header1,
                header2=header2)
            updownstr = self.sequence_updown(seq1, seq2, maxwidth=79)
            diffstr_unified = difflib.unified_diff(
                seq1_str.splitlines(),
                seq2_str.splitlines(),
                fromfile=header1,
                tofile=header2,
                lineterm='',
            )
            # diffstr_ndiff = list(difflib.ndiff(seq1_str, seq2_str))
            errmsg = unicode('\n').join((
                e.message,
                '\n',
                unicode('\n').join(sidebysidestr),
                '\n',
                unicode('\n').join(diffstr_unified),
                '\n',
                # unicode('\n').join(diffstr_ndiff),
                unicode('\n').join(updownstr),
            ))
            e.message = errmsg
            print(errmsg)
            raise

    def assertTestIO(self, testio, msg=None):
        """
        Args:
            testio (test_pyline.IO):
        Kwargs:
            msg (None, str): Assertion kwargs
        """
        # print(testio)
        args, kwargs, expectedoutput = testio

        if isinstance(args, basestring):
            args = args.splitlines(True)
        iterable = args

        if hasattr(expectedoutput, 'readlines'):
            expectedoutputlist = expectedoutput.readlines()
        elif hasattr(expectedoutput, 'splitlines'): # isinstance(basestring)
            expectedoutputlist = expectedoutput.splitlines(True)
        else:
            expectedoutputlist = expectedoutput

        # output = list(pyline.pyline(args, **kwargs)) # TODO: port sort?

        output = []
        pyline.main(iterable=iterable, results=output, opts=kwargs)

        outputresults = [x.result for x in output]
        self.assertSequenceEqualSidebyside(
                expectedoutputlist,
                outputresults,
                seq_type=list, # (list, io.StringIO),
                header1='seq1',
                header2='seq2',
                msg=msg)


class LoggingTestCase():
    def setup_logging(self):
        self.log = logging.getLogger() # self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)


class TestPyline(
    SequenceTestCase, LoggingTestCase, unittest.TestCase):

    def setUp(self, *args):
        self.setup_logging()

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
        _test_input = io.StringIO(TEST_INPUT)
        for test in PYLINE_TESTS:
            for line in pyline.pyline(_test_input, **test):
                print(line, file=_test_output)

    def test_15_pyline_sort__0__line_asc0(self):
        io = IO(TEST_INPUT_A0,
                {"cmd": "line", "sort_asc": "0"},
                TEST_OUTPUT_A0_SORT_ASC_0.splitlines(True))
        self.assertTestIO(io)

    def test_15_pyline_sort__1__words_asc0(self):
        io = IO(TEST_INPUT_A0,
                {"cmd": "words", "sort_asc": "0"},
                splitwords(TEST_OUTPUT_A0_SORT_ASC_0))
        self.assertTestIO(io)

    def test_15_pyline_sort__2__words_asc1(self):
        io = IO(TEST_INPUT_A0,
                {"cmd": "words", "sort_asc": "1"},
                splitwords(TEST_OUTPUT_A0_SORT_ASC_1))
        self.assertTestIO(io)

    def test_15_pyline_sort__3__words_asc2(self):
        io = IO(TEST_INPUT_A0,
                {"cmd": "words", "sort_asc": "2"},   # words[2]
                splitwords(TEST_OUTPUT_A0_SORT_ASC_2))
        self.assertTestIO(io)

    def test_15_pyline_sort__4__line_asc1(self):
        io = IO(TEST_INPUT_A0,
                {"cmd": "line", "sort_asc": "1"},    # line[2] == ' ' # XXX
                TEST_INPUT_A0.splitlines(True))
        self.assertTestIO(io)

    def test_15_pyline_sort__5__words_desc2(self):
        io = IO(TEST_INPUT_A0,
                {"cmd": "words", "sort_desc": "2"},  # words[2]
                splitwords(TEST_OUTPUT_A0_SORT_DESC_2))
        self.assertTestIO(io)

    # def test_15_pyline_sort__6(self):
    #     # TODO: AssertRaises ? output w/ cmd "line" undef.
    #     pass

    # def test_15_pyline_sort__7(self):
    #     io = ({"cmd": "line", "sort_desc": "0"},
    #           TEST_OUTPUT_A0_SORT_DESC_0)
    #     self.assertTestIO(io)

    # def test_15_pyline_sort__8(self):
    #     io = ({"cmd": "words", "sort_desc": "0"},
    #           splitwords(TEST_OUTPUT_A0_SORT_DESC_0))
    #     self.assertTestIO(io)

    # def test_15_pyline_sort__9(self):
    #     io = ({"cmd": "words"},
    #           TODO)
    #     self.assertTestIO(io)

    # def test_15_pyline_sort__10(self):
    #     io = ({"cmd": "w[:3]"},
    #           TODO)
    #     self.assertTestIO(io)

    # def test_15_pyline_sort__11(self):
    #     io = ({"regex": r"(.*)"},
    #           TODO)
    #     self.assertTestIO(io)

    # def test_15_pyline_sort__12(self):
    #     io = ({"regex": r"(.*)", "cmd": "rgx and rgx.groups()"},
    #           TODO)
    #     self.assertTestIO(io)

    # def test_15_pyline_sort__13(self):
    #     io = ({"regex": r"(.*)", "cmd": "rgx and rgx.groups() or '#'"},
    #           TODO)
    #     self.assertTestIO(io)


class TestPylineMain(LoggingTestCase, unittest.TestCase):

    def setUp(self):
        self.setup_logging()
        self.setup_TEST_FILE()

    def setup_TEST_FILE(self):
        (self._test_file_fd, self.TEST_FILE) = tempfile.mkstemp(text=True)
        fd = self._test_file_fd
        if IS_PYTHON2:
            os.write(fd, TEST_INPUT)
            os.write(fd, self.TEST_FILE)
        else:
            os.write(fd, TEST_INPUT.encode('utf8'))
            os.write(fd, self.TEST_FILE.encode('utf8'))

        self.log.info("setup: %r", repr(self.TEST_FILE))

    def tearDown(self):
        os.close(self._test_file_fd)
        os.remove(self.TEST_FILE)

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
            # TODO: decide what to do about sorted([('a', '1'), ('b', None)])
            ("w", '-O', 'csv', '-s', '1'),
            ("w", '-O', 'csv', '-s', '1,2'),
            ("w", '-O', 'csv', '-S', '1'),
            ("w", '-O', 'csv', '-S', '1', '-n'),

            ("w", '-O', 'json'),
            ("w", '-O', 'json', '-n'),

            ("w", '-O', 'tsv'),

            ("w", '-O', 'html'),

            ("w", '-O', 'checkbox'),
            ("w", '-O', 'chk'),

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
                output = pyline.main(_args)
                for n in output and output or []:
                    self.log.debug(n)
            except Exception as e:
                self.log.error("cmd: %s" % repr(_args))
                self.log.exception(e)
                raise

class TestPylineConsoleMain(unittest.TestCase):
    def test_pyline_console_main_0(self):
        # note: this expects that pyline is installed with either:
        #   python setup.py develop # or
        #   python setup.py install
        from distutils.spawn import find_executable
        pyline_bin = find_executable('pyline')
        self.assertTrue(pyline_bin)
        cmd = [pyline_bin, '--help']
        import subprocess
        ret = subprocess.check_call(cmd)
        self.assertEqual(ret, 0)

class TestPylinePyline(SequenceTestCase, unittest.TestCase):
    def test_30_pyline_codefunc(self):
        iterable = ["one", "two"]
        outrable = ["eno", "owt"]

        codefunc = lambda x: x['line'][::-1]
        output = pyline.pyline(iterable, codefunc=codefunc)
        self.assertTrue(isinstance(output, types.GeneratorType))
        output_list = [result.result for result in output]
        self.assertEqual(output_list, outrable)  # ...

        cmd = 'line[::-1]'
        output2 = pyline.pyline(iterable, cmd=cmd)
        self.assertTrue(isinstance(output2, types.GeneratorType))
        output_list2 = [result.result for result in output2]
        self.assertEqual(output_list2, outrable)  # ...


import types

class TestColspec(unittest.TestCase):

    colspecstr_inputs = """
    0
    0,1,2'
    2, 1, 0
    2:int
    0:str, 1:int, 2:int
    0:int, 1:int, 2:int  # raises
    0, 1, 2:int
    2::int, 2::xsd:integer  #
    #0:"xsd:string", 2:xsd:integer #
    attr:"xsd:string", attr2:"xsd:integer" #
    """
    def test_parse_colspecstr(self):
        for x in map(str.lstrip, self.colspecstr_inputs.splitlines()):
            def _fut(x):  # "function under test"
                return pyline.parse_colspecstr(x)
            output = _fut(x)
            self.assertTrue(output)
            self.assertIsInstance(output, types.GeneratorType)
            #TODO

def wrap_in_pylineresult(iterable, uri=None, meta=None):
    for i, x in enumerate(iterable):
        yield pyline.PylineResult(
            n=i,
            result=x)
        # ,
        #     uri=uri,
        #     meta=meta)


class TestSortfunc(SequenceTestCase, unittest.TestCase):
    def test_sort_by_001(self):
        iterable = splitwords(TEST_INPUT_A0)
        resiterable = wrap_in_pylineresult(iterable)
        # output = pyline.sort_by(resiterable, sortstr='1')
        output = pyline.sort_by(resiterable, sortstr='1', reverse=False)
        self.assertIsInstance(output, list)
        self.assertTrue(output)
        expectedoutput = splitwords(TEST_OUTPUT_A0_SORT_ASC_1)
        expectedoutputresults = list(
            wrap_in_pylineresult(expectedoutput[::-1]))[::-1]  # TEST_INPUT_A0
        self.assertSequenceEqualSidebyside(expectedoutputresults, output)
        self.assertSequenceEqual(expectedoutputresults, output)
        self.assertEqual(expectedoutputresults, output)


class Test_parse_formatstring(unittest.TestCase):

    def assertFormatString(self, input_, expectedoutput):
        output = pyline.parse_formatstring(input_)
        expectedoutput = pyline.OrderedDict_(expectedoutput)
        self.assertDictEqual(expectedoutput, output)
        self.assertEqual(expectedoutput, output)

    def test_parse_formatstring__01(self):
        dict = pyline.OrderedDict_
        self.assertFormatString(
            'format',
            dict((('_output_format', 'format'), ('_output_format_args', None))))
        self.assertFormatString(
            'format:opt1',
            dict((('_output_format', 'format'), ('_output_format_args', 'opt1'),
                  ('opt1', True))))
        _output_formatstring = 'format:+isTrue,isTrue2,-isFalse,key0=value0,key1=1,key21=2.1'
        self.assertFormatString(
            _output_formatstring,
            dict((('_output_format', 'format'),
                  ('_output_format_args', _output_formatstring[7:]),
                 ('isTrue', True),
                 ('isTrue2', True),
                 ('isFalse', False),
                 ('key0', 'value0'),
                 ('key1', 1),
                 ('key21', 2.1),
            )))
        _output_formatstring = 'format:+isTrue,isTrue2,-isFalse,key0=value0,key1=1,key21=2.1'
        self.assertFormatString(
            _output_formatstring,
            dict((('_output_format', 'format'),
                  ('_output_format_args', _output_formatstring[7:]),
                 ('isTrue', True),
                 ('isTrue2', True),
                 ('isFalse', False),
                 ('key0', 'value0'),
                 ('key1', 1),
                 ('key21', 2.1),
            )))
        self.assertFormatString(
            ':opt1',
            dict((('_output_format', None),
                  ('_output_format_args', 'opt1'),
                  ('opt1', True),
                  )))
        self.assertFormatString(
            ':',
            dict((('_output_format', None),
                  ('_output_format_args', None))))
        self.assertFormatString(
            '',
            dict((('_output_format', None),
                  ('_output_format_args', None))))


class Test_str2boolintorfloat(unittest.TestCase):

    def test_str2boolintorfloat_01(self):
        str2boolintorfloat = pyline.str2boolintorfloat
        self.assertEqual(
            str2boolintorfloat('true'),
            True)
        self.assertEqual(
            str2boolintorfloat('True'),
            True)
        self.assertEqual(
            str2boolintorfloat('false'),
            False)
        self.assertEqual(
            str2boolintorfloat('False'),
            False)
        self.assertEqual(
            str2boolintorfloat('0'),
            0)
        self.assertEqual(
            str2boolintorfloat('0.1'),
            0.1)
        teststr = 'test "string" '
        self.assertEqual(
            str2boolintorfloat(teststr),
            teststr)
        self.assertEqual(
            str2boolintorfloat(''),
            '')

jinja2 = None

class TestPylineJinja(unittest.TestCase):
    def setUp(self):
        global jinja2
        import jinja2

    def test_pyline_jinja__mustspecifyargs_ValueError(self):
        iterable = TEST_INPUT_A0
        with self.assertRaises(ValueError):
            pyline.main(
                args=['-O', 'jinja'],
                iterable=iterable)

    def test_pyline_jinja__TemplateNotFound(self):
        iterable = TEST_INPUT_A0
        results = []
        with self.assertRaises(jinja2.TemplateNotFound):
            pyline.main(
                args=['-O', 'jinja:template=TemplateNotFound!.jinja'],
                results=results,
                iterable=iterable)

    def test_pyline_jinja__testtemplate(self):
        iterable = TEST_INPUT_A0
        template_name = 'obj-newline.jinja2'
        templatespath = os.path.realpath(os.path.join(
            os.path.dirname(__file__),
            '..',
            'pyline',
            'templates'))
        templatepath = os.path.join(templatespath, template_name)
        output_formatstr = 'jinja:template={}'.format(templatepath)
        results = []
        retcode, _results = pyline.main(
            #args=['-O', 'jinja:template=obj-newline.jinja'],
            args=['-O', output_formatstr],
            results=results,
            iterable=iterable)
        self.assertEqual(0, retcode)
        self.assertEqual(results, _results)

if __name__ == '__main__':
    sys.exit(unittest.main())
