# -*- coding: utf-8 -*-


class MockWindow:
    def show_quick_panel(options, done):
        return False

    def show_input_panel(caption, text, done, change, cancel):
        return False


class MockSublime:
    def active_window():
        return False
