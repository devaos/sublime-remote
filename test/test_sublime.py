# -*- coding: utf-8 -*-

import sys
import unittest

import env
import mocks.sublime
sys.modules['sublime'] = mocks.sublime.MockSublime()
import remote.sublime as sublime_api


class TestSublimeHelperFunctions(unittest.TestCase):
    def test_active_project_bad_args(self):
        w = mocks.sublime.MockWindow()
        ret = sublime_api.project_by_file(w, None)
        self.assertEqual(ret, None, 'Bad arguments should return nothing')

    def test_update_project_settings(self):
        w = mocks.sublime.MockWindow()
        w.set_project_data({"folders": [{"path": "/a"}]})
        ret = sublime_api.update_project_settings(w, "/a/b", {"a": "b"})
        self.assertIsNot(ret, None, 'Settings should change')
        self.assertDictEqual(ret, {'a': 'b', 'path': '/a'},
                             'Settings should match')


suite = unittest.TestLoader().loadTestsFromTestCase(TestSublimeHelperFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
