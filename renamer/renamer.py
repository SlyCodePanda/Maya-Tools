from maya import cmds


# A class that holds all the UI details for the Renamer window and its functionality.
class RenamerWindow(object):
    windowName = "Renamer"
    height = 370
    width = 300

    # UI

    def show(self):
        # If a window named "Renamer" already exists, delete the UI.
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        # Create the window, build the UI, then show the window.
        self.window = cmds.window(self.windowName, w=self.width, h=self.height, mnb=False, mxb=False, sizeable=False)
        self.buildUI()
        cmds.showWindow()
        cmds.setFocus(self.windowName)

    # Reset all text fields.
    def reset(self, *args) :
        cmds.textField(self.searchField, edit=True, text='')
        cmds.textField(self.replaceField, edit=True, text='')

        cmds.textField(self.prefixField, edit=True, text='')
        cmds.textField(self.suffixField, edit=True, text='')

        cmds.textField(self.renameField, edit=True, text='')
        cmds.textField(self.startField, edit=True, text='1')
        cmds.textField(self.paddingField, edit=True, text='0')

    # Close the Renamer window.
    def close(self, *args) :
        cmds.deleteUI(self.windowName)

    def buildUI(self):
        textWidth = 45
        fieldWidth = 250
        buttonWidth = 295

        cmds.setParent(self.window)

        # Main layout.
        mainColumnLayout = cmds.columnLayout(w=self.width, h=self.height)

        # Search and Replace.
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Search:", align='right', w=textWidth)
        self.searchField = cmds.textField(w=fieldWidth, ann="Search field")

        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Replace:", align='right', w=textWidth)
        self.replaceField = cmds.textField(w=fieldWidth, ann="Replace field")

        cmds.setParent('..')

        cmds.separator(h=5)
        cmds.button("Search and Replace", w=buttonWidth, align='centre', command=self.searchAndReplace,
                    ann="Search for object and rename it")

        cmds.separator(h=20, style='in')

        # Prefix.
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Prefix:", align='right', w=textWidth)
        self.prefixField = cmds.textField(w=fieldWidth, ann="Prefix field")

        cmds.setParent('..')

        cmds.separator(h=5)
        cmds.button("Add Prefix", w=buttonWidth, align='centre', command=self.addPrefix,
                    ann="Add prefix to selected object(s)")

        cmds.separator(h=20, style='in')

        # Suffix.
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Suffix:", align='right', w=textWidth)
        self.suffixField = cmds.textField(w=fieldWidth, ann="Prefix field")

        cmds.setParent('..')

        cmds.separator(h=5)
        cmds.button("Add Suffix", w=buttonWidth, align='centre', command=self.addSuffix,
                    ann="Add suffix to selected object(s)")

        cmds.separator(h=20, style='in')

        # Rename and Number.
        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Rename:", align='right', w=textWidth)
        self.renameField = cmds.textField(w=fieldWidth, ann="Rename field")

        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Start #:", align='right', w=textWidth)
        self.startField = cmds.textField(w=50, text=1, ann="Starting number field")

        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="Padding:", align='right', w=textWidth)
        self.paddingField = cmds.textField(w=50, text=0, ann="Padding field")

        cmds.setParent('..')

        cmds.button("Rename and Number", w=buttonWidth, align='center', command=self.renameAndNumber,
                    ann="Rename and number objects with defined number padding")
        cmds.separator(h=20, style='in')

        cmds.setParent('..')


        cmds.rowLayout(numberOfColumns=2)
        cmds.button("Reset", w=buttonWidth/2.01, align='center', command=self.reset, ann="Reset all fields")
        cmds.button("Close", w=buttonWidth / 2.01, align='center', command=self.close, ann="Close window")

    # RENAMER PROCS

    # Searches for an object of given name and renames it another given name.
    def searchAndReplace(self, *args):
        # Search and Replace queries.
        search = cmds.textField(self.searchField, q=True, text=True)
        replace = cmds.textField(self.replaceField, q=True, text=True)

        # First check if the searched for object exists, if it exists, rename it.
        if cmds.objExists(search):
            cmds.rename(search, replace)
        else:
            cmds.error("The object %s does not exist." % search)


    # Add prefix to a list of objects.
    def addPrefix(self, *args):
        prefix = cmds.textField(self.prefixField, q=True, text=True)
        objects = cmds.ls(selection=True, long=True)

        for i in range(len(objects)):
            # Get the name of the current object in the list.
            oldName = objects[i].split("|")[-1]
            newName = ""

            if prefix:
                newName = "%s%s" % (prefix, oldName)

            cmds.rename(oldName, newName)


    # Add prefix to a list of objects.
    def addSuffix(self, *args):
        suffix = cmds.textField(self.suffixField, q=True, text=True)
        objects = cmds.ls(selection=True, long=True)

        for i in range(len(objects)):
            # Get the name of the current object in the list.
            oldName = objects[i].split("|")[-1]
            newName = ""

            if suffix:
                newName = "%s%s" % (oldName, suffix)

            cmds.rename(oldName, newName)


    # Renames and numbers objects with chosen padding to the number.
    def renameAndNumber(self, *args):
        rename = cmds.textField(self.renameField, q=True, text=True)
        start = int(cmds.textField(self.startField, q=True, text=True))
        padding = cmds.textField(self.paddingField, q=True, text=True)
        objects = cmds.ls(selection=True, long=True)
        paddingLength = len(padding)

        for i in range(len(objects)):
            oldName = objects[i].split("|")[-1]
            newName = rename + (str(start).zfill(paddingLength))
            cmds.rename(oldName, newName)
            start += 1













