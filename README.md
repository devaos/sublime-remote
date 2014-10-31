#sublime-remote
[![Build Status](https://travis-ci.org/devaos/sublime-remote.svg?branch=master)](https://travis-ci.org/devaos/sublime-remote) [![Coverage Status](https://coveralls.io/repos/devaos/sublime-remote/badge.png)](https://coveralls.io/r/devaos/sublime-remote)

Provides rsync and scp facilities to automatically sync a remote host when editing files locally.

##Limitations

* This plugin requires Sublime Text 3
* This plugin is not Windows compatible

##Installation

You can install the plugin simply by cloning it into Sublime 3 plugin directory:

```bash
git clone https://github.com/devaos/sublime-remote.git ~/Library/Application Support/Sublime Text 3/Packages/Remote
```

##Use

###Map a remote directory to your local project directory

* Right-click on a project folder in your side-bar and select Remote > Map to Remote...
* Enter the remote host and path, as you would with scp or rsync ("host:/path").  You can optionally use "vagrant" as the host.
* If you entered "vagrant" it will auto-select the vagrant VM if you only have 1 running, otherwise it will prompt you to select which vagrant VM you wish to map.

Once the project directory is mapped, anytime you save a file Sublime will attempt to scp the file to the remote host.

###Sync a local directory from a remote host

* Right-click on a project folder in your side-bar and select Remote > Rsync Local from Remote.
* If you have not already mapped the project folder to a remote host, it will take you through the process described above.

The contents of the remote host will then be copied into the local project folder.