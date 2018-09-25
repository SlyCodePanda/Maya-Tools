from maya import cmds
# Using pymel.all for it's Callback function.
from pymel.all import *



# RENAMER PROCS

# Adds a prefix OR suffix to the list of objects given.
def addPrefixOrSuffix(prefix, suffix):
    objects = cmds.ls(selection=True, long=True)
    for i in range(len(objects)):
        # Get the name of the current object in the list.
        oldName = objects[i].split("|")[-1]
        newName = ""
        if prefix:
            newName = "%s%s" % (prefix, oldName)
        if suffix:
            newName = "%s%s" % (oldName, suffix)

        cmds.rename(oldName, newName)


# Searches for an object of given name and renames it another given name.
# def searchAndReplace(search, replace):
#     # First check if the searched for object exists, if it exists, rename it.
#     if cmds.objExists(search):
#         cmds.rename(search, replace)
#     else:
#         cmds.warning("The object %s does not exist." % search)


# Renames and numbers objects with chosen padding to the number.
def renameAndNumber(rename, start, padding):
    objects = cmds.ls(selection=True, long=True)
    paddingLength = len(padding)

    for i in range(len(objects)):
        oldName = objects[i].split("|")[-1]

        newName = rename + (str(start).zfill(paddingLength))
        cmds.rename(oldName, newName)
        start += 1




# A class that holds all the UI details for the Renamer window.
class RenamerWindow(object):
    windowName = "Renamer"
    height = 330
    width = 300

    # UI

    def show(self):
        # If a window named "Renamer" already exists, delete the UI.
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        # Create the window, build the UI, then show the window.
        self.window = cmds.window(self.windowName, w=self.width, h=self.height, mnb=False, sizeable=False)
        self.buildUI()
        cmds.showWindow()


    def buildUI(self):
        textWidth = 45
        fieldWidth = 250
        buttonWidth = 295

        cmds.setParent(self.window)

        # Main layouts.
        mainColumnLayout = cmds.columnLayout(w=self.width, h=self.height)

        # Search and Replace.
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Search:", align='right', w=textWidth)
        self.searchField = cmds.textField(w=fieldWidth, editable=True)

        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Replace:", align='right', w=textWidth)
        self.replaceField = cmds.textField(w=fieldWidth, editable=True)

        cmds.setParent('..')

        cmds.separator(h=5)
        cmds.button("Search and Replace", w=buttonWidth, align='centre',
                    command=Callback(self.searchAndReplace))

        cmds.separator(h=20, style='in')


        # Prefix.
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Prefix:", align='right', w=textWidth)
        cmds.textField(w=fieldWidth)

        cmds.setParent('..')

        cmds.separator(h=5)
        cmds.button("Add Prefix", w=buttonWidth, align='centre')

        cmds.separator(h=20, style='in')


        # Suffix.
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Suffix:", align='right', w=textWidth)
        cmds.textField(w=fieldWidth)

        cmds.setParent('..')

        cmds.separator(h=5)
        cmds.button("Add Suffix", w=buttonWidth, align='centre')

        cmds.separator(h=20, style='in')


        # Rename and Number.
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Rename:", align='right', w=textWidth)
        cmds.textField(w=fieldWidth)

        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Start #:", align='right', w=textWidth)
        cmds.textField(w=50, text=1)

        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Padding:", align='right', w=textWidth)
        cmds.textField(w=50, text=0)

        cmds.setParent('..')

        cmds.button("Rename and Number", w=buttonWidth, align='center')

    # RENAMER PROCS

    # Searches for an object of given name and renames it another given name.
    def searchAndReplace(self):
        # Search and Replace queries.
        search = cmds.textField(self.searchField, q=1, text=1)
        replace = cmds.textField(self.replaceField, q=1, text=1)

        # First check if the searched for object exists, if it exists, rename it.
        if cmds.objExists(search):
            cmds.rename(search, replace)
        else:
            cmds.warning("The object %s does not exist." % search)













