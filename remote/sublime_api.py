# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ari Aosved
# http://github.com/devaos/sublime-remote/blob/master/LICENSE

import sublime

# =============================================================================


def project_by_file(projects, filename):
    """Returns the project entry which matches the path of the file."""

    if type(projects) != dict or projects.get('folders', None) is None:
        return None

    for folder in projects['folders']:
        if filename.startswith(folder['path']) \
           and folder.get('remotePath', None) is not None:
            return folder

    return None


def show_quick_panel(options, done):
    w = sublime.active_window()
    w.show_quick_panel(options, done)


def show_input_panel(caption, text, done, change, cancel):
    w = sublime.active_window()
    w.show_input_panel(caption, text, done, change, cancel)
