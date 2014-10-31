# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ari Aosved
# http://github.com/devaos/sublime-remote/blob/master/LICENSE

"""This module implements an API layer for Vagrant related functionality."""

import subprocess

# =============================================================================


def get_ssh_settings(vm):
    p1 = subprocess.Popen(["/usr/bin/vagrant", "ssh-config", "33ca156"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    p2 = subprocess.Popen(["/usr/bin/awk", "-v", "ORS= ",
                          '{if($1 && $2){print "-o " $1 "=" $2}}'],
                          stdin=p1.stdout, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    opt = ""
    while True:
        buf = p2.stdout.readline()
        decoded = buf.decode("utf-8").rstrip()
        if decoded == '' and p2.poll() is not None:
            break
        if decoded == '':
            continue
        opt += decoded

        return opt

    return opt
