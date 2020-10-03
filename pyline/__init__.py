#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from . import pyline
    __version__ = version = pyline.version
except AttributeError:
    pass  # TODO

# __main__ = pyline.main_entrypoint
