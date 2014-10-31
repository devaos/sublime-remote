# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ari Aosved
# http://github.com/devaos/sublime-remote/blob/master/LICENSE

"""This module implements the Sublime Text 3 commands provided by remote."""

import os
import re
import sys
import sublime
import sublime_plugin
import subprocess
import threading

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import remote.sublime_api as sublime_api
import remote.sync_api as sync_api
import remote.vagrant_api as vagrant_api

# =============================================================================


class AddRemoteCommand(sublime_plugin.TextCommand):
    """Map a new remote path to a local project path."""

    def run(self, edit, paths):
        print("Local path", paths[0])
        addRemoteThread = AddRemoteThread(paths[0])
        addRemoteThread.start()


class AddRemoteThread(threading.Thread):
    """Don't lock up Sublime while we configure ourselves."""

    localPath = ""
    remotePath = ""
    vm = ""

    def __init__(self, localPath):
        self.localPath = localPath
        threading.Thread.__init__(self)

    # =========================================================================

    def run(self):
        p1 = subprocess.Popen(["/usr/bin/vagrant", "global-status"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        opt = ['Select VM below...', '---']
        while True:
            buf = p1.stdout.readline()
            decoded = buf.decode("utf-8").rstrip()
            if decoded == '' and p1.poll() is not None:
                break
            if decoded == '':
                continue
            parts = re.split('\s+', decoded)
            if len(parts) == 5 and parts[0] != 'id' \
               and re.match('^[0-9a-f]{1,7}$', parts[0]):
                opt.append(decoded)

        def done_with_vm(i=-1):
            if i == -1:
                return False
            parts = re.split('\s+', opt[i])
            if len(parts) != 5 or parts[0] == 'id' \
               or re.match('^[0-9a-f]{1,7}$', parts[0]) is None:
                return False
            self.vm = parts[0]
            print("VM selected", self.vm)

            ssh = vagrant_api.get_ssh_settings(self.vm)
            if ssh == '':
                return False

            if sync_api.rsync(self.localPath, self.remotePath, ssh) is True:
                w = sublime.active_window()
                sublime_api.update_project_settings(w, self.localPath, {
                                                    "remotePath":
                                                    self.remotePath,
                                                    "remoteOptions": ssh})

        def done_with_folder(remotePath):
            print("Remote path", remotePath)
            parts = remotePath.split(':')
            if len(parts) == 2 and parts[0] == 'vagrant':
                self.remotePath = remotePath
                sublime.set_timeout(lambda: sublime_api.show_quick_panel(
                                    opt, done_with_vm), 10)

        sublime.set_timeout(lambda: sublime_api.show_input_panel(
                            "Sync remote to this folder", "", done_with_folder,
                            None, None), 10)

# =============================================================================


class RemoteEdit(sublime_plugin.EventListener):
    """Sync a local change out."""

    def on_post_save(self, view):
        remoteEditThread = RemoteEditThread(view.file_name())
        remoteEditThread.view = view
        remoteEditThread.start()


class RemoteEditThread(threading.Thread):
    """Don't lock up Sublime while we configure ourselves."""

    view = None

    # =========================================================================

    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename

    # =========================================================================

    def run(self):
        filename = self.filename
        w = sublime.active_window()

        found = sublime_api.project_by_file(w, filename)
        if found is None:
            return False

        return sync_api.scp(found['path'], filename, found['remotePath'],
                            found['remoteOptions'])
