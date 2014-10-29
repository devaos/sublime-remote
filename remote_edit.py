# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ari Aosved
# http://github.com/devaos/sublime-remote/blob/master/LICENSE

import sublime
import sublime_plugin
import threading
import subprocess
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import remote.sublime_api as sublime_api

# =============================================================================


class RemoteEdit(sublime_plugin.EventListener):
    def on_post_save(self, view):
        remoteEditThread = RemoteEditThread(view.file_name())
        remoteEditThread.view = view
        remoteEditThread.start()

# =============================================================================


class RemoteEditThread(threading.Thread):
    view = None

    # =========================================================================

    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename

    # =========================================================================

    def show_quick_panel(self, options, done):
        w = self.view.window()
        w.show_quick_panel(options, done)

    # =========================================================================

    def run(self):

        filename = self.filename
        w = sublime.active_window()

        found = sublime_api.project_by_file(w.project_data(), filename)
        if found is None:
            return False

        target = "'$1' '$2$3'"
        target = target.replace("$1", filename)
        target = target.replace("$2", found['remotePath'])
        target = target.replace("$3", filename[len(found['path'])+1:])

        cmd = "scp " + found['remoteOptions'] + " " + target

        print("Scp command", cmd)

        ret = subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
        if ret != 0:
            print("Scp failed with", ret)
            return False

        return True
