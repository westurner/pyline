#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

if sys.version_info.major > 2:
    import pyline.pyline as pyline
else:
    import pyline

__version__ = version = pyline.version

# __main__ = pyline.main_entrypoint
