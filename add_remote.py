# -*- coding: utf-8 -*-

import sublime, sublime_plugin, threading, subprocess, re

#===============================================================================

class AddRemoteCommand(sublime_plugin.TextCommand):
  def run(self, edit, paths):
    print("Local path", paths[0])
    addRemoteThread = AddRemoteThread(paths[0])
    addRemoteThread.start()

#===============================================================================

class AddRemoteThread(threading.Thread):
  localPath = ""
  remotePath = ""
  vm = ""

  def __init__(self, localPath):
    self.localPath = localPath
    threading.Thread.__init__(self)

  #=============================================================================

  def show_quick_panel(self, options, done):
    w = sublime.active_window()
    w.show_quick_panel(options, done)

  def show_input_panel(self, caption, text, done, change, cancel):
    w = sublime.active_window()
    w.show_input_panel(caption, text, done, change, cancel)

  #=============================================================================

  def ssh_opt(self, vm):
    p1 = subprocess.Popen(["/usr/bin/vagrant", "ssh-config", "33ca156"],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    p2 = subprocess.Popen(["/usr/bin/awk", "-v", "ORS= ",
      '{if($1 && $2){print "-o " $1 "=" $2}}'], stdin=p1.stdout,
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    opt = ""
    while True:
      buf = p2.stdout.readline()
      decoded = buf.decode("utf-8").rstrip()
      if decoded == '' and p2.poll() != None: break
      if decoded == '': continue
      opt += decoded

    return opt

  #=============================================================================

  def rsync(self):
    opt = self.ssh_opt(self.vm)
    if opt == '':
      return False

    if re.match('/$', self.remotePath) == None:
      self.remotePath += "/"

    cmd = "/usr/bin/rsync -e 'ssh " + opt + "' -avz '" + self.remotePath \
      + "' '" + self.localPath + "'"

    print("Rsync command", cmd)

    ret = subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
    if ret != 0:
      print("Rsync failed with", ret)
      return False

    w = sublime.active_window()
    settings = w.project_data()
    print("Project settings", settings)

    changed = False
    for folder in settings['folders']:
      if folder['path'] == self.localPath:
        print("Folder settings", folder)
        folder['remotePath'] = self.remotePath
        folder['remoteOptions'] = opt
        changed = True

    if changed:
      print("New project settings", settings)
      w.set_project_data(settings)

  #=============================================================================

  def run(self):
    p1 = subprocess.Popen(["/usr/bin/vagrant", "global-status"],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    opt = ['Select VM below...','---']
    while True:
      buf = p1.stdout.readline()
      decoded = buf.decode("utf-8").rstrip()
      if decoded == '' and p1.poll() != None: break
      if decoded == '': continue
      parts = re.split('\s+', decoded)
      if len(parts) == 5 and parts[0] != 'id' and re.match('^[0-9a-f]{1,7}$', parts[0]):
        opt.append(decoded)

    def done_with_vm(i):
      parts = re.split('\s+', opt[i])
      if len(parts) != 5 or parts[0] == 'id' or re.match('^[0-9a-f]{1,7}$', parts[0]) == None:
        return False
      self.vm = parts[0]
      print("VM selected", self.vm)
      self.rsync()

    def done_with_folder(remotePath):
      print("Remote path", remotePath)
      parts = remotePath.split(':')
      if len(parts) == 2 and parts[0] == 'vagrant':
        self.remotePath = remotePath
        sublime.set_timeout(lambda: self.show_quick_panel(opt, done_with_vm),
          10)

    sublime.set_timeout(lambda: self.show_input_panel(
      'Sync remote to this folder', '', done_with_folder, None, None), 10)
