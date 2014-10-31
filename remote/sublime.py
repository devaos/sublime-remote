# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ari Aosved
# http://github.com/devaos/sublime-remote/blob/master/LICENSE

"""This module implements an API layer for Sublime related functionality."""

import sublime

# =============================================================================


def project_by_file(window, filename):
    """Returns the project folder which matches the base path of the file."""

    if window is None:
        return None

    projects = window.project_data()

    if type(projects) != dict or projects.get('folders', None) is None:
        return None

    for folder in projects['folders']:
        if filename.startswith(folder['path']) \
           and folder.get('remotePath', None) is not None:
            return folder

    return None


def update_project_settings(window, filename, settings):
    """Update the settings associated with a specific project folder."""

    if window is None:
        return None

    projects = window.project_data()

    if type(projects) != dict or projects.get('folders', None) is None:
        return None

    for folder in projects['folders']:
        if filename.startswith(folder['path']):
            print("Folder settings", folder)
            for k in iter(settings):
                folder[k] = settings[k]
            print("New folder settings", folder)

            window.set_project_data(projects)
            return folder

    return None


def show_quick_panel(options, done):
    w = sublime.active_window()
    w.show_quick_panel(options, done)


def show_input_panel(caption, text, done, change, cancel):
    w = sublime.active_window()
    w.show_input_panel(caption, text, done, change, cancel)
