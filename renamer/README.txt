Script:     | renamer.py
Authors:    | Renee Marsland
Required:   | maya.cmds
            | renamer.py
Desc:       | Quickly rename objects in the outliner. Allows you to search replace words in names, add suffixes and               prefixes, as well as adding numbering with specified padding.

Usage:

Download, extract and place script into maya's script directories.
In Python, run-

import renamer
reload(renamer)
renamer.RenamerWindow().show()
