# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ari Aosved
# http://github.com/devaos/sublime-remote/blob/master/LICENSE

import re
import subprocess

# =============================================================================


def rsync(localPath, remotePath, sshSettings):
    opts = []
    if sshSettings != "":
        opts.append("-e 'ssh " + sshSettings + "'")
    opts.append("-avz")

    if re.match('/$', remotePath) is None:
        remotePath += "/"

    cmd = "/usr/bin/rsync " + " ".join(opts) \
        + " '" + remotePath + "'" \
        + " '" + localPath + "'"

    print("Rsync command", cmd)

    ret = subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
    if ret != 0:
        print("Rsync failed with", ret)
        return False

    return True


def scp(localProjectPath, localPath, remotePath, sshSettings):
    target = "'$1' '$2$3'"
    target = target.replace("$1", localPath)
    target = target.replace("$2", remotePath)
    target = target.replace("$3", localPath[len(localProjectPath)+1:])

    cmd = "scp " + sshSettings + " " + target

    print("Scp command", cmd)

    ret = subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
    if ret != 0:
        print("Scp failed with", ret)
        return False

    return True
