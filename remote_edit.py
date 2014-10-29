import sublime, sublime_plugin, threading, subprocess

class RemoteEdit(sublime_plugin.EventListener):
  def on_post_save(self, view):
    remoteEditThread = RemoteEditThread(view.file_name())
    remoteEditThread.view = view
    remoteEditThread.start()

class RemoteEditThread(threading.Thread):
  view = None

  def __init__(self, fileName):
      threading.Thread.__init__(self)
      self.fileName = fileName

  def show_quick_panel(self, options, done):
    w = self.view.window()
    w.show_quick_panel(options, done)

  def run(self):
    fileName = self.fileName

    w = sublime.active_window()
    settings = w.project_data()

    found = None
    for folder in settings['folders']:
      if fileName.startswith(folder['path']) and folder.get('remotePath', None) != None:
        found = folder
        break

    if found == None:
      return False

    target = "'$1' '$2$3'"
    target = target.replace( "$1", fileName )
    target = target.replace( "$2", found['remotePath'] )
    target = target.replace( "$3", fileName[len(folder['path'])+1:] )

    cmd = "scp " + found['remoteOptions'] + " " + target

    print("Scp command", cmd)

    ret = subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
    if ret != 0:
      print("Scp failed with", ret)
      return False

    return True