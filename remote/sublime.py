# -*- coding: utf-8 -*-

def findProjectByFile(projects, filename):
  if type(projects) != dict or projects.get('folders', None) == None:
    return None

  for folder in projects['folders']:
    if filename.startswith(folder['path']) and folder.get('remotePath', None) != None:
      return folder
  return None