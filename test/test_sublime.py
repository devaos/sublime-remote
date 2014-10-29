# -*- coding: utf-8 -*-

import sys
import unittest
import env
import remote.sublime

class TestSublimeHelperFunctions(unittest.TestCase):
  def test_active_project_bad_args(self):
    ret = remote.sublime.findProjectByFile(None, None)
    self.assertEqual(ret, None, 'Bad arguments should return nothing')

suite = unittest.TestLoader().loadTestsFromTestCase(TestSublimeHelperFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
