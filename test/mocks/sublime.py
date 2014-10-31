# -*- coding: utf-8 -*-


class MockWindow:
    _project_data = {}

    def show_quick_panel(self, options, done):
        return False

    def show_input_panel(self, caption, text, done, change, cancel):
        return False

    def project_data(self):
        return self._project_data

    def set_project_data(self, data):
        self._project_data = data
        return True


class MockSublime:
    def active_window():
        return False
