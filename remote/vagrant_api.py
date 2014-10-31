# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ari Aosved
# http://github.com/devaos/sublime-remote/blob/master/LICENSE

"""This module implements an API layer for Vagrant related functionality."""

import re
import subprocess

# =============================================================================


def parse_vm_id(line):
    """Determine if a line appears to be from `vagrant global-status`."""

    parts = re.split("\s+", line)
    if len(parts) == 5 and parts[0] != "id" \
       and re.match("^[0-9a-f]{1,7}$", parts[0]):
        return parts[0]

    return None


def get_vm_list(opt):
    """Pull a list of all running vagrant VMs for the user to choose from."""

    p1 = subprocess.Popen(["/usr/bin/vagrant", "global-status"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        buf = p1.stdout.readline()
        decoded = buf.decode("utf-8").rstrip()
        if decoded == "" and p1.poll() is not None:
            break
        if decoded == "":
            continue
        if parse_vm_id(decoded) is not None:
            opt.append(decoded)

    return opt


def get_ssh_options(vm):
    """Pull the ssh options required to connect to a specific vagrant VM."""

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
        if decoded == "" and p2.poll() is not None:
            break
        if decoded == "":
            continue
        opt += decoded

        return opt

    return opt
