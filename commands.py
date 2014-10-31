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
        sublime.set_timeout_async(lambda: add_remote_async(paths[0], None), 0)


def add_remote_async(path, callback):
    print("Local path", path)

    def done_with_folder(userInput):
        print("Remote path", userInput)
        parts = userInput.split(":")
        if len(parts) == 2 and parts[0] == "vagrant":
            vms = ["Select VM below...", "---"]
            vagrant_api.get_vm_list(vms)
            if len(vms) == 3:
                done_with_vm(userInput, vms, 2)
            else:
                sublime_api.show_quick_panel(vms,
                                             lambda i=-1:
                                             done_with_vm(userInput, vms, i))
        else:
            do_it(userInput, "")

    def done_with_vm(remotePath, vms, userSelection):
        if userSelection == -1:
            return False

        vm = vagrant_api.parse_vm_id(vms[userSelection])
        if vm is None:
            return False
        print("VM selected", vm)

        sshOptions = vagrant_api.get_ssh_options(vm)

        if sshOptions != "":
            do_it(remotePath, sshOptions)

    def do_it(remotePath, sshOptions):
        w = sublime.active_window()
        settings = {"remotePath": remotePath, "remoteOptions": sshOptions}
        sublime_api.update_project_settings(w, path, settings)
        if callback is not None:
            callback(settings)

    sublime_api.show_input_panel("Sync remote to this folder", "",
                                 done_with_folder, None, None)

# =============================================================================


class FromRemote(sublime_plugin.TextCommand):
    """Sync a local directory from  a remote directory."""

    def run(self, edit, paths):
        sublime.set_timeout_async(lambda: from_remote_async(paths[0]), 0)


def from_remote_async(path):
    print("Local path", path)
    w = sublime.active_window()

    found = sublime_api.project_by_path(w, path)
    if found is None or found["remotePath"] == "":
        add_remote_async(path, lambda o: sync_api.rsync_from_remote(path,
                         o["remotePath"], o["remoteOptions"]))
        return True

    return sync_api.rsync_from_remote(found["path"], found["remotePath"],
                                      found["remoteOptions"])

# =============================================================================


class RemoteEdit(sublime_plugin.EventListener):
    """Sync a local change out."""

    def on_post_save_async(self, view):
        filename = view.file_name()
        w = sublime.active_window()

        found = sublime_api.project_by_path(w, filename)
        if found is None:
            return False

        return sync_api.scp_to_remote(found["path"], filename,
                                      found["remotePath"],
                                      found["remoteOptions"])
