# -*- coding:utf8 -*-
from __future__ import print_function, absolute_import, unicode_literals
"""Mybot test cases
"""

import os
from errbot.backends.test import testbot


class TestMyPlugin(object):
    extra_plugin_dir = os.path.dirname(os.path.abspath(__file__))

    def test_run_city(self, testbot):
        testbot.push_message('!jpweather_city')
        assert u'東京' in testbot.pop_message()

    def test_run_area(self, testbot):
        testbot.push_message('!jpweather_area')
        assert u'東京都' in testbot.pop_message()
