# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ari Aosved
# http://github.com/devaos/sublime-remote/blob/master/LICENSE

"""This module implements an API layer for sync related shell commands."""

import os
import re
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import remote.sublime_api as sublime_api

# =============================================================================


def default_rsync_options():
    return "-rlz --delete"


def rsync_remote(fromPath, toPath, sshSettings, rsyncOptions):
    """Sync from a location to another location."""

    if fromPath is None or toPath is None:
        return False

    if len(fromPath) == 0 or len(toPath) == 0:
        return False

    opts = default_rsync_options() + " "

    if rsyncOptions is not None and len(rsyncOptions) > 0:
        opts = rsyncOptions + " "

    if sshSettings != "":
        opts += "-e 'ssh " + sshSettings + "'"

    if re.match("/$", fromPath) is None:
        fromPath += "/"

    toPath = re.sub("/$", "", toPath)

    rsync = "/usr/bin/rsync "
    cmd = rsync + opts + " '" + fromPath + "'" + " '" + toPath + "'"

    doit = sublime_api.ok_cancel_dialog("Are you sure you want to run the" +
                                        " following command? It will" +
                                        " overwrite the target" +
                                        " directory.\n\n" + cmd)

    if doit is not True:
        return False

    print("Rsync command", cmd)

    try:
        subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError:
        sublime_api.error_message("Rsync command failed. Check path and" +
                                  " permissions")
        return False

    return True


def rsync_remote_file(localProjectPath, localPath, remotePath, sshSettings,
                      rsyncOptions):
    """Sync a single local file to remote."""

    if localProjectPath is None or localPath is None or remotePath is None:
        return False

    if len(localProjectPath) == 0 or len(localPath) == 0 or \
       len(remotePath) == 0:
        return False

    opts = default_rsync_options() + " "

    if rsyncOptions is not None and len(rsyncOptions) > 0:
        opts = rsyncOptions + " "

    if sshSettings != "":
        opts += "-e 'ssh " + sshSettings + "'"

    if re.match("/$", localProjectPath) is None:
        localProjectPath += "/"

    remotePath = re.sub("/$", "", remotePath)

    rsync = "/usr/bin/rsync "
    cmd = rsync + opts + " '" + localPath + "' '" + remotePath + \
        "/" + localPath[len(localProjectPath):] + "'"

#    doit = sublime_api.ok_cancel_dialog("Are you sure you want to run the" +
#                                        " following command? It will" +
#                                        " overwrite the target" +
#                                        " file.\n\n" + cmd)
#
#    if doit is not True:
#        return False

    print("Rsync command", cmd)

    try:
        subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError:
        sublime_api.error_message("Scp command failed. Check path and" +
                                  " permissions")
        return False

    return True
