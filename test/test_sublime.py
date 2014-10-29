# -*- coding: utf-8 -*-

import sys
import unittest

import env
import mocks.sublime
sys.modules['sublime'] = mocks.sublime.MockSublime()
import remote.sublime_api as sublime_api


class TestSublimeHelperFunctions(unittest.TestCase):
    def test_active_project_bad_args(self):
        ret = sublime_api.project_by_file(None, None)
        self.assertEqual(ret, None, 'Bad arguments should return nothing')

suite = unittest.TestLoader().loadTestsFromTestCase(TestSublimeHelperFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
