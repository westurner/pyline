#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pyline setup.py
"""

import glob
import logging
import os
import subprocess
import sys

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

CONFIG = {
    'debug': True,
    'logname': None,
    'logformat': '%(asctime)s %(name)s %(levelname)-5s %(message)s',
    'loglevel': logging.DEBUG,  # logging.INFO
}

logging.basicConfig(format=CONFIG['logformat'])
log = logging.getLogger(CONFIG['logname'])
log.setLevel(CONFIG['loglevel'])

SETUPPY_PATH = os.path.dirname(os.path.abspath(__file__)) or '.'
log.debug('SETUPPY_PATH: %s' % SETUPPY_PATH)


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTestCommand(Command):
    user_options = []
    description = "Run runtests.py with the current sys.executable"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cmd = [sys.executable,
               "-m", "pytest",
               "-v",
               os.path.join(SETUPPY_PATH, "tests/"),
        ]

        cmdstr = ' '.join(cmd)
        print(cmdstr)
        log.info(cmdstr)

        errno = subprocess.call(cmd)
        raise SystemExit(errno)


def build_long_description():
    with open('README.rst') as f:
        readme = f.read()
    with open('HISTORY.rst') as f:
        history = f.read().replace('. :changelog:', '')
    with open('AUTHORS.rst') as f:
        authors = f.read()
    return readme + '\n\n' + history + '\n\n' + authors


setup(
    name='pyline',
    version='0.3.19',
    description=(
        'Pyline is a grep-like, sed-like, awk-like command-line tool '
        'for line-based text processing in Python.'),
    long_description=build_long_description(),
    long_description_content_type='text/x-rst',
    author='Wes Turner',
    author_email='wes@wrd.nu',
    url='https://github.com/westurner/pyline',
    download_url='https://github.com/westurner/pyline/releases',
    packages=[
        'pyline',
    ],
    package_dir={'pyline':
                 'pyline'},
    include_package_data=True,
    install_requires=[],
    license="PSF",
    zip_safe=False,
    keywords='pyline sed grep',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'pyline=pyline.pyline:main_entrypoint'
        ]
    },
    test_suite='tests',
    cmdclass={
        'test': PyTestCommand,
    }
)
