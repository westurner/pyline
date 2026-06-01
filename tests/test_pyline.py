#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_pyline
----------------------------------

Tests for `pyline` module.
"""
from __future__ import print_function
import collections
import difflib
# import json
import importlib
import logging
import os
import pprint
import runpy
import sys
import tempfile
import types
import unittest
from unittest import mock

try:
    from itertools import izip_longest  # type: ignore
except ImportError:
    from itertools import zip_longest as izip_longest

try:
    import StringIO as io  # type: ignore
except ImportError:
    import io

pyline = importlib.import_module('pyline.pyline')

IS_PYTHON2 = sys.version_info.major == 2

if not IS_PYTHON2:  # pragma: no branch
    basestring = str
    unicode = str

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
    line for line in TEST_OUTPUT_A0_SORT_ASC_2.splitlines()[::-1]
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
        obj1_repr_maxwidth = 0
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
            errmsg = '\n'.join((
                str(e),
                '\n',
                '\n'.join(sidebysidestr),
                '\n',
                '\n'.join(diffstr_unified),
                '\n',
                # unicode('\n').join(diffstr_ndiff),
                '\n'.join(updownstr),
            ))
            print(errmsg)
            raise AssertionError(errmsg)

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

            ("w", '-O', 'jsonlines'),
            ("w", '-O', 'jsonlines', '-n'),
            ("w", '-O', 'jsonl'),
            ("w", '-O', 'jsonl', '-n'),

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
            ("-p", "p and p.is_file() and (p.size, p, p.stat())"),
            ("--pathlib", "p and p.is_file() and (os.path.getsize(p), p, os.stat(p))")
        )

        TEST_ARGS = ('-f', self.TEST_FILE)

        for argset in CMDLINE_TESTS:
            with self.subTest(args=argset):
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
        try:
            from shutil import which as find_executable
        except ImportError:
            from distutils.spawn import find_executable  # type: ignore
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

        def codefunc(ctxt):
            return ctxt['line'][::-1]

        output = pyline.pyline(iterable, codefunc=codefunc)
        self.assertTrue(isinstance(output, types.GeneratorType))
        output_list = [result.result for result in output]
        self.assertEqual(output_list, outrable)  # ...

        cmd = 'line[::-1]'
        output2 = pyline.pyline(iterable, cmd=cmd)
        self.assertTrue(isinstance(output2, types.GeneratorType))
        output_list2 = [result.result for result in output2]
        self.assertEqual(output_list2, outrable)  # ...


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
        if jinja2 is None:
            try:
                jinja2 = importlib.import_module('jinja2')
            except ImportError:
                self.skipTest('jinja2 is not installed')

    def test_pyline_jinja__mustspecifyargs_ValueError(self):
        iterable = TEST_INPUT_A0
        with self.assertRaises(ValueError):
            pyline.main(
                args=['-O', 'jinja'],
                iterable=iterable)

    def test_pyline_jinja__TemplateNotFound(self):
        iterable = TEST_INPUT_A0
        results = []
        with self.assertRaises(getattr(jinja2, 'TemplateNotFound')):
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


class TestCoverageTargets(unittest.TestCase):
    def test_pyline_result_branches(self):
        none_result = pyline.PylineResult(n=1, result=None)
        self.assertIsNone(none_result.__str__())
        self.assertEqual([1, None], list(none_result._numbered()))

        false_result = pyline.PylineResult(n=2, result=False)
        self.assertFalse(false_result.__str__())
        self.assertEqual([2, False], list(false_result._numbered()))

        dict_result = pyline.PylineResult(n=3, result=collections.OrderedDict((('a', 1), ('b', 2))))
        self.assertEqual('1\t2', str(dict_result))
        self.assertEqual([3, 1, 2], list(dict_result._numbered()))

        str_result = pyline.PylineResult(n=4, result='abc\n')
        self.assertEqual('abc', str(str_result))
        self.assertEqual([4, 'abc'], list(str_result._numbered()))

        iter_result = pyline.PylineResult(n=5, result=('x', 'y'))
        self.assertEqual('x\ty', str(iter_result))
        self.assertEqual([5, 'x', 'y'], list(iter_result._numbered()))
        self.assertIn('x', iter_result._numbered_str(odelim='|'))

    def test_log_helper_paths(self):
        self.assertEqual(('a', {'k': 'v'}), pyline.log_('a', k='v'))
        self.assertEqual((('a', 'b'), {'k': 'v'}), pyline.log_('a', 'b', k='v'))
        self.assertEqual({}, pyline.log_())

    def test_parse_field_and_colspec_paths(self):
        with mock.patch('pdb.set_trace', return_value=None):
            self.assertEqual('alpha', pyline.parse_field('alpha', shlex=False))
            self.assertEqual('alpha beta', pyline.parse_field('"alpha beta"', shlex=True))
            cols = list(pyline.parse_colspecstr('0::int, 1::xsd:string'))
            self.assertEqual('0', cols[0][0])
            self.assertEqual(int, cols[0][1])
            self.assertEqual('1', cols[1][0])
            self.assertEqual(str, cols[1][1])

    def test_sort_by_error_paths(self):
        with self.assertRaises(AttributeError):
            list(pyline.sort_by(
                [pyline.PylineResult(n=0, result=['x'])],
                sortstr='0',
                col_map={'0': int},
            ))

        with self.assertRaises(TypeError):
            pyline.sort_by(
                [
                    pyline.PylineResult(n=0, result=['1']),
                    pyline.PylineResult(n=1, result=[1]),
                ],
                sortstr='0',
            )

    def test_result_writer_paths(self):
        output = io.StringIO()
        writer = pyline.ResultWriter.get_writer(output, output_format='txt', number_lines=True)
        writer.output_func(pyline.PylineResult(n=1, result=('a', 'b')))
        self.assertIn('a\tb', output.getvalue())

        with self.assertRaises(ValueError):
            pyline.ResultWriter.get_writer(io.StringIO(), output_format='unknown')

        html_writer = pyline.ResultWriter_html(io.StringIO())
        html_writer.header(attrs=['col'])
        html_writer.write(pyline.PylineResult(n=1, result=1))
        html_writer.footer()
        self.assertIn('<table>', html_writer._output.getvalue())

        base_writer = pyline.ResultWriter(io.StringIO())
        with self.assertRaises(Exception):
            base_writer.set_output(io.StringIO())

    def test_get_sort_function_and_main_opts_paths(self):
        with self.assertRaises(ValueError):
            pyline.get_sort_function(sort_asc='0', sort_desc='0')

        null_sort = pyline.get_sort_function()
        data = [pyline.PylineResult(n=0, result=['a'])]
        self.assertEqual(data, list(null_sort(data)))

        with self.assertRaises(ValueError):
            pyline.main(opts=object(), iterable=['x'])

    def test_main_entry_and_branch_paths(self):
        out = io.StringIO()
        retcode, _ = pyline.main(
            args=['-r', '(?P<line>.*<.*)', '-O', 'json'],
            iterable=['<x>\n'],
            output=out,
        )
        self.assertEqual(0, retcode)
        self.assertIn('line', out.getvalue())

        with mock.patch.object(pyline, 'get_sort_function', return_value=None):
            out2 = io.StringIO()
            retcode2, results2 = pyline.main(
                args=['line'],
                iterable=['x\n'],
                output=out2,
                results=[],
            )
            self.assertEqual(0, retcode2)
            self.assertEqual(1, len(results2))

        with mock.patch.object(pyline, 'get_sort_function', return_value=None):
            retcode3, results3 = pyline.main(
                args=['None'],
                iterable=['x\n'],
                output=io.StringIO(),
                results=[],
            )
            self.assertEqual(0, retcode3)
            self.assertEqual([], results3)

        with mock.patch.object(pyline, 'main_entrypoint') as mocked_main:
            runpy.run_module('pyline.__main__', run_name='__main__')
            mocked_main.assert_called_once_with()

        with mock.patch.object(pyline, 'main_entrypoint') as mocked_main2:
            importlib.reload(importlib.import_module('pyline.__main__'))
            mocked_main2.assert_not_called()

    def test_main_closes_real_file_handle(self):
        with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf8') as tf:
            tf.write('one\n')
            tf.flush()
            path = tf.name
        try:
            file_handle = open(path, 'r', encoding='utf8')
            self.assertFalse(file_handle.closed)
            pyline.main(args=['line'], iterable=file_handle, output=io.StringIO())
            self.assertTrue(file_handle.closed)
        finally:
            os.remove(path)

    def test_pyline_additional_internal_branches(self):
        real_import = __import__

        def _import(name, *args, **kwargs):
            if name == 'path':
                raise ImportError('forced for coverage test')
            return real_import(name, *args, **kwargs)

        with mock.patch('builtins.__import__', side_effect=_import):
            with self.assertRaises(ImportError):
                list(pyline.pyline(['x\n'], cmd='line', path_tools_pathpy=True))

        shlex_output = list(pyline.pyline(['"a b" c\n'], cmd='words', shlex=True))
        self.assertEqual(['a b', 'c'], shlex_output[0].result)

        ilast_output = list(pyline.pyline(['a\n', 'b\n'], cmd='(i_last, line)'))
        self.assertEqual(2, ilast_output[0].result[0])

        with self.assertRaises(ZeroDivisionError):
            list(pyline.pyline(['a\n'], cmd='1/0'))

        with self.assertRaises(ZeroDivisionError):
            list(pyline.pyline(['a\n'], codefunc=lambda ctxt: 1 / 0))

    def test_datasource_and_build_column_map_paths(self):
        ds = pyline.PylineDatasource(results=[])
        ds.add_resultset(None)
        self.assertIn('resultsets', ds.data)

        ds2 = pyline.PylineDatasource()
        self.assertEqual([], ds2.data['resultsets'])

        existing = collections.OrderedDict((('0', int),))
        self.assertIs(existing, pyline.build_column_map(existing))
        self.assertEqual(collections.OrderedDict(), pyline.build_column_map(None))

    def test_parse_field_error_and_numeric_parse_exception_path(self):
        with mock.patch('pdb.set_trace', return_value=None):
            with self.assertRaises(ValueError):
                pyline.parse_field('   ', shlex=True)

        class BadMatch(object):
            def group(self, *_args, **_kwargs):
                raise IndexError('no group')

        with mock.patch.object(pyline.re, 'match', return_value=BadMatch()):
            self.assertEqual('123', pyline.str2boolintorfloat('123'))

    def test_main_option_branches(self):
        with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf8') as tf:
            tf.write('x\0y\0')
            tf.flush()
            src_path = tf.name
        out_path = src_path + '.out'
        try:
            read0_out = io.StringIO()
            read0_ret, _ = pyline.main(args=['-f', src_path, '--read0', 'line'], output=read0_out)
            self.assertEqual(0, read0_ret)
            self.assertEqual(['x', 'y'], read0_out.getvalue().splitlines())

            ret, _ = pyline.main(
                args=['-f', src_path, '-o', out_path, 'line'],
                output=None,
            )
            self.assertEqual(0, ret)
            self.assertTrue(os.path.exists(out_path))
        finally:
            if os.path.exists(src_path):
                os.remove(src_path)
            if os.path.exists(out_path):
                os.remove(out_path)

    def test_main_entrypoint_in_pyline_module(self):
        with mock.patch.object(pyline, 'main', return_value=(0, [])):
            with mock.patch.object(sys, 'argv', ['pyline']):
                with self.assertRaises(SystemExit) as exc:
                    pyline.main_entrypoint()
                self.assertEqual(0, exc.exception.code)

    def test_remaining_branch_targets(self):
        class RStripOnly(object):
            def __init__(self, value):
                self.value = value

            def __getitem__(self, item):
                return self.value[item]

            def rstrip(self):
                return self.value.rstrip()

        rs = pyline.PylineResult(n=1, result=RStripOnly('abc\n'))
        self.assertEqual('abc', rs.__str__())
        self.assertEqual('abc', rs.__unicode__())

        rs_no_nl = pyline.PylineResult(n=2, result=RStripOnly('abc'))
        self.assertIsInstance(rs_no_nl.__str__(), RStripOnly)

        iter_empty = pyline.PylineResult(n=9, result=tuple())
        self.assertEqual([9], list(iter_empty._numbered()))

        with self.assertRaises(Exception):
            pyline.debug('x')

        default_cmd = list(pyline.pyline(['x\n']))
        self.assertEqual('x\n', default_cmd[0].result)

        pathlib_cmd = list(pyline.pyline(['x\n'], path_tools_pathlib=True))
        self.assertTrue(pathlib_cmd[0].result)

        with self.assertRaises(SyntaxError):
            list(pyline.pyline(['x\n'], cmd='x['))

        join_cmd = list(pyline.pyline(['x\n'], cmd='j([1,2])'))
        self.assertEqual('1\t2', join_cmd[0].result)

        with self.assertRaises(UnboundLocalError):
            list(pyline.pyline(['x\n'], cmd=''))

        class BrokenLine(str):
            def endswith(self, *_args, **_kwargs):
                raise RuntimeError('boom')

        broken = BrokenLine('abc\n')
        broken_path = list(pyline.pyline([broken], cmd='line', path_tools_pathlib=True))
        self.assertEqual('abc\n', broken_path[0].result)

        self.assertEqual([2], pyline.OrderedDict_({1: 2}).values())

        self.assertEqual([], list(pyline.parse_colspecstr('')))
        with mock.patch('pdb.set_trace', return_value=None):
            with self.assertRaises(UnboundLocalError):
                list(pyline.parse_colspecstr('0'))

        with mock.patch('pdb.set_trace', return_value=None):
            mapped = pyline.build_column_map('0::int')
        self.assertIn('0', mapped)

        sorted_no_sortstr = pyline.sort_by(
            [pyline.PylineResult(n=0, result=['b']), pyline.PylineResult(n=1, result=['a'])],
            sortstr=None,
        )
        self.assertEqual('a', sorted_no_sortstr[0].result[0])

        class MsgValueError(ValueError):
            def __init__(self):
                super(MsgValueError, self).__init__('bad')
                self.msg = 'bad'

        def bad_cast(_value):
            raise MsgValueError()

        with self.assertRaises(MsgValueError):
            pyline.sort_by(
                [pyline.PylineResult(n=0, result=['z'])],
                sortstr='0',
                col_map={'0': bad_cast},
            )

        w = pyline.ResultWriter(None)
        w.set_output(io.StringIO())
        self.assertIsNotNone(w._output)

        out = io.StringIO()
        base_writer = pyline.ResultWriter(out)
        base_writer.write_numbered('abc')
        self.assertIn('abc', out.getvalue())

        csv_out = io.StringIO()
        csv_writer = pyline.ResultWriter_csv(csv_out)
        csv_writer.header(attrs=['a', 'b'])
        self.assertIn('"a"', csv_out.getvalue())

        class TrulyEmpty(object):
            pass

        with self.assertRaises(KeyError):
            pyline.main(opts=TrulyEmpty(), output=io.StringIO())

        class EmptyOpts(object):
            def __init__(self):
                self.file = '-'
                self.output = '-'

        with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf8') as sf:
            sf.write('stdin line\n')
            sf.flush()
            sf.seek(0)
            with mock.patch.object(sys, 'stdin', sf):
                ret_stdin, _ = pyline.main(opts=EmptyOpts(), output=io.StringIO())
        self.assertEqual(0, ret_stdin)

        with mock.patch.object(pyline, 'get_sort_function', return_value=None):
            ret_nosort, res_nosort = pyline.main(
                args=['line'],
                iterable=['x\n', 'y\n'],
                output=io.StringIO(),
                results=[],
            )
            self.assertEqual(0, ret_nosort)
            self.assertEqual(2, len(res_nosort))

        ret_v, _ = pyline.main(opts={'verbose': True, 'cmd': 'line'}, iterable=['x\n'], output=io.StringIO())
        self.assertEqual(0, ret_v)

        ret_q, _ = pyline.main(opts={'quiet': True, 'cmd': 'line'}, iterable=['x\n'], output=io.StringIO())
        self.assertEqual(0, ret_q)

        ret_ver, no_results = pyline.main(opts={'version': True}, iterable=['x\n'], output=io.StringIO())
        self.assertEqual(0, ret_ver)
        self.assertIsNone(no_results)

        with mock.patch('pdb.set_trace', return_value=None):
            ret_cols, _ = pyline.main(
                opts={'cmd': 'line', 'col_mapstr': '0::int'},
                iterable=['1\n'],
                output=io.StringIO(),
            )
        self.assertEqual(0, ret_cols)

        with self.assertRaises(SystemExit):
            pyline.main(opts={'cmd': 'line', 'sort_asc': '0', 'sort_desc': '0'}, iterable=['1\n'], output=io.StringIO())

        ret_skip, _ = pyline.main(args=['None'], iterable=['x\n'], output=io.StringIO())
        self.assertEqual(0, ret_skip)


if __name__ == '__main__':
    unittest.main()
