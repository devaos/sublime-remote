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


class RsyncOptionsCommand(sublime_plugin.TextCommand):
    """Override default rsync options for Remote."""

    def run(self, edit, paths):
        sublime.set_timeout_async(lambda: rsync_options(paths[0], None), 0)


def rsync_options(path, callback):
    print("Local path", path)
    w = sublime.active_window()

    def done_with_options(userInput):
        print("Options", userInput)

        if len(userInput) == 0:
            do_it(sync_api.default_rsync_options())
            return True

        do_it(userInput)
        return True

    def do_it(rsyncOptions):
        settings = {"rsyncOptions": rsyncOptions}
        sublime_api.update_project_settings(w, path, settings)
        if callback is not None:
            callback(settings)

    options = sync_api.default_rsync_options()
    found = sublime_api.project_by_path(w, path)
    if found is not None and found["rsyncOptions"] != "":
        options = found["rsyncOptions"]

    sublime_api.show_input_panel("Use these rsync options:",
                                 options, done_with_options, None, None)


# =============================================================================


class AddRemoteCommand(sublime_plugin.TextCommand):
    """Map a new remote path to a local project path."""

    def run(self, edit, paths):
        sublime.set_timeout_async(lambda: add_remote_async(paths[0], None), 0)


def add_remote_async(path, callback):
    print("Local path", path)
    w = sublime.active_window()

    def done_with_folder(userInput):
        print("Remote path", userInput)

        if len(userInput) == 0:
            do_it("", "")
            return True

        parts = userInput.split(":")
        if len(parts) != 2:
            sublime_api.error_message("The remote path you entered does not" +
                                      " appear to contain a host")
            return False

        more = parts[0].split("@")
        host = ""
        if len(more) > 2:
            sublime_api.error_message("Unable to parse the remote path you" +
                                      " entered")
            return False
        elif len(more) == 2:
            host = more[1]
        else:
            host = more[0]

        if host == "vagrant":
            vms = ["Select VM below...", "---"]
            vagrant_api.get_vm_list(vms)
            if len(vms) == 2:
                sublime_api.error_message("No vagrant VMs found")
                return False
            if len(vms) == 3:
                done_with_vm(userInput, vms, 2)
            else:
                sublime_api.show_quick_panel(vms,
                                             lambda i=-1:
                                             done_with_vm(userInput, vms, i))
        else:
            do_it(userInput, "")

        return True

    def done_with_vm(remotePath, vms, userSelection):
        if userSelection == -1:
            return False

        vm = vagrant_api.parse_vm_id(vms[userSelection])
        if vm is None:
            return False
        print("VM selected", vm)

        sshOptions = vagrant_api.get_ssh_options(vm)
        print("ssh options", sshOptions)

        if sshOptions != "":
            do_it(remotePath, sshOptions)

    def do_it(remotePath, sshOptions):
        settings = {"remotePath": remotePath, "remoteOptions": sshOptions}
        sublime_api.update_project_settings(w, path, settings)
        if callback is not None:
            callback(settings)

    remotePath = ""
    found = sublime_api.project_by_path(w, path)
    if found is not None and found["remotePath"] != "":
        remotePath = found["remotePath"]

    sublime_api.show_input_panel("Sync this folder to remote folder:",
                                 remotePath, done_with_folder, None, None)

# =============================================================================


class FromRemote(sublime_plugin.TextCommand):
    """Sync a local directory from a remote directory."""

    def run(self, edit, paths):
        sublime.set_timeout_async(lambda: from_remote_async(paths[0]), 0)


def from_remote_async(path):
    print("From local path", path)
    w = sublime.active_window()

    found = sublime_api.project_by_path(w, path)
    if found is None or found["remotePath"] == "":
        add_remote_async(path, lambda o: sync_api.rsync_remote(
                         o.get("remotePath", ""), path,
                         o.get("remoteOptions", ""),
                         o.get("rsyncOptions", "")))
        return True

    return sync_api.rsync_remote(found.get("remotePath", ""),
                                 found.get("path", ""),
                                 found.get("remoteOptions", ""),
                                 found.get("rsyncOptions", ""))

# =============================================================================


class ToRemote(sublime_plugin.TextCommand):
    """Sync a local directory to a remote directory."""

    def run(self, edit, paths):
        sublime.set_timeout_async(lambda: to_remote_async(paths[0]), 0)


def to_remote_async(path):
    print("To local path", path)
    w = sublime.active_window()

    found = sublime_api.project_by_path(w, path)
    if found is None or found["remotePath"] == "":
        add_remote_async(path, lambda o: sync_api.rsync_remote(path,
                         o.get("remotePath", ""),
                         o.get("remoteOptions", ""),
                         o.get("rsyncOptions", "")))
        return True

    return sync_api.rsync_remote(found.get("path", ""),
                                 found.get("remotePath", ""),
                                 found.get("remoteOptions", ""),
                                 found.get("rsyncOptions", ""))

# =============================================================================


class RemoteEdit(sublime_plugin.EventListener):
    """Sync a local change out."""

    def on_post_save_async(self, view):
        filename = view.file_name()
        w = sublime.active_window()

        found = sublime_api.project_by_path(w, filename)
        if found is None:
            return False

        return sync_api.rsync_remote_file(found.get("path", ""), filename,
                                          found.get("remotePath", ""),
                                          found.get("remoteOptions", ""),
                                          found.get("rsyncOptions", ""))
