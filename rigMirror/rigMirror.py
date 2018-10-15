from maya import cmds
import pymel.core

# A class that holds all functions for mirroring a rig.
class rigMirror(object):
    # Class variables
    connections = {}
    controls = []
    curSide = ""
    newSide = ""

    # Initializer function.
    def __init__(self, curSide, newSide):
        self.curSide = curSide
        self.newSide = newSide

        # Get the rig controls based on user selection.
        # Get both groups and any children.
        self.controls = cmds.ls(sl=True, dag=True, type="transform")

        print("CONTROLS : \n %s" % self.controls)

        self.mirrorControls()

    # Checks if node is a group.
    # Returns True if node is a group, False otherwise.
    def isGroup(self, node):
        if cmds.nodeType(node) != "transform":
            return False

        children = cmds.listRelatives(node, c=True)

        if children == None:
            return True

        for c in children:
            if cmds.nodeType(c) != 'transform':
                return False
        else:
            return True

    # Class functions
    # Takes in an object and gives it a new name whether you are creating a left or right duplicate of it.
    def getNewSideName(self, object):
        oldName = str(object)
        newName = oldName.replace(self.curSide, self.newSide)

        return newName

    # Duplicates and mirrors rig controls
    def mirrorControls(self):
        # Iterate through the controls and their groups and duplicate them.
        for control in self.controls:
            # Get the group and the control in it.
            # If selection is a group, get ctrlGrp.
            duplicate = ""
            ctrlName = str(control)

            grpName = cmds.listRelatives(ctrlName, parent=True)

            # If the object selected is a control with a group.
            if grpName != None:
                grp = cmds.listRelatives(ctrlName, parent=True)[0]
                # Duplicate groups and controls
                duplicate = cmds.duplicate(ctrlName, rr=True, name=self.getNewSideName(ctrlName))
                newGrp = cmds.group(duplicate, name=self.getNewSideName(grp), world=True)

            # Scale the group at -1 in axis you want to mirror. For now we will just do it in X-axis.
            if duplicate:
                group = cmds.listRelatives(duplicate, parent=True)
                cmds.group(group, name="ctrls_mirrorGrp")
                cmds.xform(group, os=True, piv=[0, 0, 0])
                cmds.scale(-1, 1, 1, group)
                cmds.ungroup("ctrls_mirrorGrp")

                # Freeze transforms.
                cmds.makeIdentity(group, apply=True, t=1, r=1, s=1, n=0)

                # Clear construction history.
                cmds.delete(group, constructionHistory=True)

                # Re-center pivot
                cmds.xform(group, centerPivots=True)

    # Get all the connections and store them in connections dictionary. Then set up connections on the other side.
    def mirrorConnections(self):
        pass
        # Look at mirrorJoint() command