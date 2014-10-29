# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ari Aosved
# http://github.com/devaos/sublime-remote/blob/master/LICENSE

import sublime, sublime_plugin, threading, subprocess, sys, os
import remote.sublime

class RemoteEdit(sublime_plugin.EventListener):
  def on_post_save(self, view):
    remoteEditThread = RemoteEditThread(view.file_name())
    remoteEditThread.view = view
    remoteEditThread.start()

class RemoteEditThread(threading.Thread):
  view = None

  def __init__(self, filename):
      threading.Thread.__init__(self)
      self.filename = filename

  def show_quick_panel(self, options, done):
    w = self.view.window()
    w.show_quick_panel(options, done)

  def run(self):
    filename = self.filename
    w = sublime.active_window()

    found = remote.sublime.findProjectByFile(w.project_data(), filename)
    if found == None:
      return False

    target = "'$1' '$2$3'"
    target = target.replace( "$1", filename )
    target = target.replace( "$2", found['remotePath'] )
    target = target.replace( "$3", filename[len(found['path'])+1:] )

    cmd = "scp " + found['remoteOptions'] + " " + target

    print("Scp command", cmd)

    ret = subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
    if ret != 0:
      print("Scp failed with", ret)
      return False

    return True