#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vxscreenshots
----------------------------------

Tests for `vxscreenshots` module.
"""

import unittest

from vxscreenshots import vxscreenshots
from vxscreenshots import config


class TestVxscreenshots(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_001_config(self):
        c = config.read_config()
        self.assertTrue(isinstance(c.get('vxscreenshots.database'), str))


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
