#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='pyline',
    version='0.1.0',
    description='A tool for line-based processing in Python.',
    long_description=readme + '\n\n' + history,
    author='Wes Turner',
    author_email='wes@wrd.nu',
    url='https://github.com/westurner/pyline',
    packages=[
        'pyline',
    ],
    package_dir={'pyline':
                 'pyline'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='pyline',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points={
        'console_scripts': [
            'pyline=pyline.pyline:main'
        ]
    },
    test_suite='tests',
)
